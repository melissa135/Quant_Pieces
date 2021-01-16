import pandas as pd


def data_uniform_qfq(df_raw, column, index, refer_index):
    # do not include the dividend recorded in refer_index day
    stock_dividend = 1.0
    cash_dividend = 0.0

    for i in range(index, refer_index):
        c_d = df_raw.iloc[i]['cash_dividend']
        s_d = df_raw.iloc[i]['stock_dividend']
        stock_dividend = 10*stock_dividend / (10 + s_d)
        cash_dividend = (10*cash_dividend + c_d) / (10 + s_d)

    result = df_raw.iloc[index][column]

    if (column == 'volume') or (column == 'vma5') or (column == 'vma20'):
        result = result/stock_dividend
    else:
        result = result*stock_dividend - cash_dividend

    return result


def prepare_data_uniform_qfq(df_raw, begin_index, refer_index):
    # begin_index is the earliest day that need to calculate
    # do not include the dividend recorded in refer_index day
    sd_coef_current = 1.0
    cd_coef_current = 0.0
    sd_coef_list = [sd_coef_current for _ in range(0, len(df_raw))]
    cd_coef_list = [cd_coef_current for _ in range(0, len(df_raw))]
    df_raw['sd_coef'] = sd_coef_list
    df_raw['cd_coef'] = cd_coef_list

    for i in range(refer_index-1, begin_index-1, -1):
        c_d = df_raw.iloc[i]['cash_dividend']
        s_d = df_raw.iloc[i]['stock_dividend']
        sd_coef_current = sd_coef_current * (10 + s_d) / 10
        cd_coef_current = cd_coef_current * (10 + s_d) / 10 + c_d / 10
        df_raw.loc[i, 'sd_coef'] = sd_coef_current
        df_raw.loc[i, 'cd_coef'] = cd_coef_current

    return df_raw


def get_data_uniform_qfq(df_raw, column, index):

    result = df_raw.iloc[index][column]
    sd_coef = df_raw.iloc[index]['sd_coef']
    cd_coef = df_raw.iloc[index]['cd_coef']

    if (column == 'volume') or (column == 'vma5') or (column == 'vma20'):
        result = result * sd_coef
    else:
        result = (result - cd_coef) / sd_coef

    return result

df = pd.DataFrame([[10.0, 10.0, 0, 0],
                   [10.0, 10.0, 0, 0],
                   [10.0, 10.0, 0, 0],
                   [10.0, 8.0, 0, 0],
                   [10.0, 10.0, 0, 0],
                   [10.0, 10.0, 1, 5],
                   [11.0, 20.0, 0, 0],
                   [8.0, 15.0, 5, 1],
                   [9.0, 10.0, 0, 0],
                   [10.0, 12.0, 2, 0],
                   [11.0, 10.0, 0, 2]],
                  columns=['price','volume','cash_dividend','stock_dividend'])

start_index = 2
refer_index = len(df)-1

old_price = [data_uniform_qfq(df, 'price', i, refer_index) for i in range(start_index, refer_index)]
old_volume = [data_uniform_qfq(df, 'volume', i, refer_index) for i in range(start_index, refer_index)]
print('old_price', old_price)
print('old_volume', old_volume)

df_qfq = prepare_data_uniform_qfq(df, start_index, refer_index)
new_price = [get_data_uniform_qfq(df_qfq, 'price', i) for i in range(start_index, refer_index)]
new_volume = [get_data_uniform_qfq(df_qfq, 'volume', i) for i in range(start_index, refer_index)]
print('new_price', new_price)
print('new_volume', new_volume)
