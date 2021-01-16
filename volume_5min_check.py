from database_utils import *
from config_offline import conf

db_handle = database_utils(conf['db_address'], conf['username'], conf['password'], 'stock_dev')

columns_list = conf['table_columns']['5minute_raw']
table_name = 'market_5minute_raw_399001'
'''
df_5min = db_handle.read_dataframe_from_mysql(columns_list, table_name)

volume_list = []
for i in range(0, len(df_5min)):
    time = df_5min.iloc[i]['time']
    if time == '11:25':
        volume = df_5min.iloc[i]['volume']
        if (len(volume_list)>0) and (volume/volume_list[-1]>50.0):
            date = df_5min.iloc[i]['date']
            print(date)
        volume_list.append(volume)
'''
time_list = [ '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45',
              '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '13:05',
              '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55',
              '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45',
              '14:50', '14:55', '15:00' ]
value_list = [ 0, 3057370, 3368430, 3116570, 2834470, 2561030, 2590480, 2748600, 3800740, 2395540,
               2265610, 2579760, 1978260, 1698440, 1810740, 1934480, 1989880, 1901600, 1495750, 1904480,
               1716170, 1974730, 1987820, 2143740, 1971290, 2294380, 3761180, 2777500, 2446660, 4312410,
               4057250, 3323540, 4579260, 6464760, 5191070, 5172040, 3953500, 4269410, 6143080, 5690660,
               4571170, 4709230, 5096820 ]

for i in range(0, len(time_list)):
    time = time_list[i]
    value = value_list[i]
    condition_cols = [ 'date', 'time' ]
    condition_vals = [ '20091124', time ]
    columns = [ 'volume' ]
    values = [ value ]
    flag = db_handle.update_mysql_data(table_name, condition_cols, condition_vals, columns, values)
    print('Execute result: %s'%flag)
