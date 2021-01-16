from database_utils import *
from config_offline import conf

db_handle = database_utils(conf['db_address'], conf['username'], conf['password'], 'stock_dev')

columns_list = conf['table_columns']['5minute_raw']
table_name = 'market_5minute_raw_399001'

df_5min = db_handle.read_dataframe_from_mysql(columns_list, table_name)

time_volume_list = []
time_volume = []
for i in range(0, len(df_5min)):
    date = df_5min.iloc[i]['date']
    if (i != 0) and (date != df_5min.iloc[i-1]['date']):
        if len(time_volume) == 48:
            avg_volume = sum(time_volume)/48
            for j in range(0, len(time_volume)):
                time_volume[j] = time_volume[j]/avg_volume
            time_volume_list.append(time_volume[:])
        time_volume = []
    time = df_5min.iloc[i]['time']
    volume = df_5min.iloc[i]['volume']
    time_volume.append(volume)

time_volume_sum = [ 0 for j in range(0, len(time_volume_list[0]))]
for i in range(0, len(time_volume_list)):
    for j in range(0, len(time_volume_sum)):
        time_volume_sum[j] = time_volume_sum[j] + time_volume_list[i][j]

for j in range(0, len(time_volume_sum)):
    time_volume_sum[j] = time_volume_sum[j]/len(time_volume_list)

print(time_volume_sum)
