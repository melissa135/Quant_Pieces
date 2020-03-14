from pandas.io.parsers import read_csv
from database_utils import database_utils
import pandas as pd
import time
import os


def data_uniform(df_raw,column,index,refer_index):

    stock_dividend = 1.0
    cash_dividend = 0.0
    
    for i in range(index, refer_index):
        c_d = df_raw.iloc[i]['cash_dividend']
        s_d = df_raw.iloc[i]['stock_dividend']
        stock_dividend = 10*stock_dividend / (10 + s_d)
        cash_dividend = (10*cash_dividend + c_d) / (10 + s_d)

    result = df_raw.iloc[index][column]
    
    if column == 'volume' :
        result = result/stock_dividend
    else :
        result = result*stock_dividend - cash_dividend
        
    return result

def from_minute_to_daily(df_minute_raw, stock, db_handle):
    df_daily = pd.DataFrame(columns=('date',
                                     'open','high','low','price',
                                     'volume',
                                     'cash_dividend','stock_dividend' ))
    
    cols = [ 'date', 'cash_dividend', 'stock_dividend' ]
    table_name = 'share_dividend_records'
    c_cols = [ 'stock' ]
    c_values = [ stock ]
    df_dividends = db_handle.read_dataframe_from_mysql_with_condition(cols, table_name, c_cols, c_values)
    dict_dividends = dict()
    for i in range(0, len(df_dividends)):
        date = df_dividends.iloc[i]['date']
        value = (df_dividends.iloc[i]['cash_dividend'], df_dividends.iloc[i]['stock_dividend'])
        dict_dividends[date] = value
        
    for i in range(0, int(len(df_minute_raw)/48)):
        j = i * 48
        struct_time = time.strptime(df_minute_raw.iloc[j]['date'], '%Y/%m/%d %H:%M')
        date = time.strftime('%Y/%m/%d', struct_time)
        open_ = df_minute_raw.iloc[j]['open']
        high = df_minute_raw.iloc[j]['high']
        low = df_minute_raw.iloc[j]['low']
        price = df_minute_raw.iloc[j+47]['price']
        volume = 0.0
        for k in range(j, j+48):
            if df_minute_raw.iloc[k]['high'] > high:
                high = df_minute_raw.iloc[k]['high']
            if df_minute_raw.iloc[k]['low'] < low:
                low = df_minute_raw.iloc[k]['low']
            volume = volume + df_minute_raw.iloc[k]['volume']

        c_d, s_d = 0.0, 0.0
        dividend_date = time.strftime('%Y%m%d', struct_time)
        if dividend_date in dict_dividends.keys():
            c_d, s_d = dict_dividends[dividend_date]

        row_dict = { 'date':date, 'open':open_, 'high':high, 'low':low, 'price':price, 'volume':volume,\
                     'cash_dividend':c_d, 'stock_dividend':s_d }
        df_daily = df_daily.append(row_dict, ignore_index=True)
            
    return df_daily

def none_to_raw(df_none):
    df_result = pd.DataFrame(columns=('date',
                                      'open','high','low','price',
                                      'volume',
                                      'ma5','ma10','ma20','ma60',
                                      'vma5','vma20',
                                      'cash_dividend','stock_dividend' ))
            
    for i in range(60,len(df_none)): # suppose the date is increasing
        dt = df_none.iloc[i]['date']
        op = df_none.iloc[i]['open']
        hg = df_none.iloc[i]['high']
        lw = df_none.iloc[i]['low']
        pr = df_none.iloc[i]['price']
        vl = df_none.iloc[i]['volume']

        sum5,sum10,sum20,sum60 = 0.0, 0.0, 0.0, 0.0
        for j in range(i,i-5,-1):
            price = data_uniform(df_none,'price',j,i)
            sum5 = sum5 + price/5.0
        for j in range(i,i-10,-1):
            price = data_uniform(df_none,'price',j,i)
            sum10 = sum10 + price/10.0
        for j in range(i,i-20,-1):
            price = data_uniform(df_none,'price',j,i)
            sum20 = sum20 + price/20.0
        for j in range(i,i-60,-1):
            price = data_uniform(df_none,'price',j,i)
            sum60 = sum60 + price/60.0

        vsum5,vsum20 = 0.0, 0.0
        for j in range(i,i-5,-1):
            volume = data_uniform(df_none,'volume',j,i)
            vsum5 = vsum5 + volume/5.0
        for j in range(i,i-20,-1):
            volume = data_uniform(df_none,'volume',j,i)
            vsum20 = vsum20 + volume/20.0

        cd = df_none.iloc[i]['cash_dividend']
        sd = df_none.iloc[i]['stock_dividend']

        row = pd.DataFrame([dict(date = dt,
                                 open = op, high = hg, low = lw, price = pr,
                                 volume = vl,
                                 ma5 = sum5, ma10 = sum10, ma20 = sum20, ma60 = sum60,
                                 vma5 = vsum5, vma20 = vsum20,
                                 cash_dividend = cd, stock_dividend = sd ),])
        df_result = df_result.append(row,ignore_index=True)
        
    return df_result


if __name__ == '__main__':
        
    src_minute_folder = '../tmp/stock_minute_target'
    src_daily_folder = '../tmp/stock_daily_aliyun/raw_data'
    dst_folder = '../tmp/stock_raw_target'
    db_handle = database_utils('localhost', 'root', '123', 'stock_dev')

    for root, _, fnames in os.walk(src_minute_folder):
        for fname in fnames:
            stock = fname.split('_')[0]
            print(stock)
            
            path = os.path.join(root, fname)
            df_minute_raw = read_csv(path)
            start_index_2019 = 0
            while df_minute_raw.iloc[start_index_2019]['date'].split('/')[0] != '2019':
                start_index_2019 = start_index_2019 + 1
            df_minute_raw_after2019 = df_minute_raw.iloc[start_index_2019:]

            df_daily_after2019 = from_minute_to_daily(df_minute_raw_after2019, stock, db_handle)
            
            path2 = os.path.join(src_daily_folder, '%s_raw.csv'%stock)
            df_daily_raw = read_csv(path2)
            df_daily_raw_select = df_daily_raw[['date','open','high','low','price','volume','cash_dividend','stock_dividend']]
            start_index_2019 = 0
            while df_daily_raw.iloc[start_index_2019]['date'].split('/')[0] != '2019':
                start_index_2019 = start_index_2019 + 1
                
            df_daily_after2019 = pd.concat([df_daily_raw_select.iloc[start_index_2019-60:start_index_2019],\
                                            df_daily_after2019])

            df_result_after2019 = none_to_raw(df_daily_after2019)

            df_result = pd.concat([df_daily_raw.iloc[:start_index_2019], df_result_after2019])
            filename = os.path.join(dst_folder, '%s_raw.csv'%stock)
            df_result.to_csv(filename)

