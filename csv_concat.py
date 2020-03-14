import os
import time
import pandas as pd

base_dir1 = '/home/zhu/workspace/tmp/stock_minute'
base_dir2 = '/home/zhu/workspace/tmp/stock_minute_aliyun/raw_5min_data'
target_dir = '/home/zhu/workspace/tmp/stock_minute_target'

for root, _, fnames in os.walk(base_dir1):
    for fname in fnames:
        print(fname)
        path1 = os.path.join(root, fname)
        path2 = os.path.join(base_dir2, fname)
        patht = os.path.join(target_dir, fname)

        df1 = pd.read_csv(path1)
        df1_date = []
        df1_volume = []
        for i in range(0, len(df1)):
            date = time.strptime(df1.iloc[i]['date'], '%Y-%m-%d %H:%M:%S')
            df1_date.append(time.strftime('%Y/%m/%d %H:%M', date))
            df1_volume.append(int(df1.iloc[i]['volume']/100))
            
        df1 = pd.DataFrame.from_dict({'date':df1_date,\
                                      'high':df1['high'],\
                                      'low':df1['low'],\
                                      'open':df1['open'],\
                                      'price':df1['close'],\
                                      'volume':df1_volume})
        
        df2 = pd.read_csv(path2)
        i = 0
        date_2019 = time.strptime('2019-01-01 00:00', '%Y-%m-%d %H:%M')
        date_2020 = time.strptime('2020-01-01 00:00', '%Y-%m-%d %H:%M')
        
        while time.strptime(':'.join(df2.iloc[i]['date'].split(':')[:2]), '%Y/%m/%d %H:%M') < date_2019:
            i = i + 48
        j = i
        while time.strptime(':'.join(df2.iloc[j]['date'].split(':')[:2]), '%Y/%m/%d %H:%M') < date_2020:
            j = j + 48

        new_df = pd.concat([df2.iloc[0:i], df1, df2.iloc[j:]])
        new_df.to_csv(patht)
        
        
