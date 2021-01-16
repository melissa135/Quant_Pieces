import pandas as pd
from database_utils import *

db_handle = database_utils(conf['db_address'], conf['username'], conf['password'], 'stock_dev')

input_table = '5minute_raw'
table_schema = conf['table_schema']['5minute_raw']
table_columns = conf['table_columns']['5minute_raw']

prefix = 'market'
suffix = ['399001']

for sf in suffix:
    '''
    input_table_name = '_'.join([prefix, input_table, sf])
    df_raw = db_handle.read_dataframe_from_mysql(table_columns, input_table_name)

    modify_count = 0
    for i in range(0, len(df_raw)-6):
        if (df_raw.iloc[i]['time'] == '13:00') and (df_raw.iloc[i+6]['time'] == '13:35'):
            df_raw.loc[i,'time'] = '13:05'
            df_raw.loc[i+1,'time'] = '13:10'
            df_raw.loc[i+2,'time'] = '13:15'
            df_raw.loc[i+3,'time'] = '13:20'
            df_raw.loc[i+4,'time'] = '13:25'
            df_raw.loc[i+5,'time'] = '13:30'
            modify_count = modify_count + 1

    del_command = 'drop table if exists %s;'%input_table_name
    try:
        db_handle.cursor.execute(del_command)
        db_handle.db.commit()
    except Exception as e:
        print(e)
        db_handle.db.rollback()

    output_table_name = input_table_name
    db_handle.create_table_if_not_exists(output_table_name, table_schema)
    db_handle.write_dataframe_to_mysql(df_raw, table_columns, output_table_name)

    print('modify %d in table %s'%(modify_count, input_table_name))
    '''
    other_table_name = '_'.join([prefix, '5minute_train', sf])
    del_command = 'drop table if exists %s;'%other_table_name
    try:
        db_handle.cursor.execute(del_command)
        db_handle.db.commit()
    except Exception as e:
        print(e)
        db_handle.db.rollback()

prefix = 'stock'
suffix = conf['stock_list']

for sf in suffix:
    '''
    input_table_name = '_'.join([prefix, input_table, sf])
    df_raw = db_handle.read_dataframe_from_mysql(table_columns, input_table_name)

    modify_count = 0
    for i in range(0, len(df_raw)-6):
        if (df_raw.iloc[i]['time'] == '13:00') and (df_raw.iloc[i+6]['time'] == '13:35'):
            df_raw.loc[i,'time'] = '13:05'
            df_raw.loc[i+1,'time'] = '13:10'
            df_raw.loc[i+2,'time'] = '13:15'
            df_raw.loc[i+3,'time'] = '13:20'
            df_raw.loc[i+4,'time'] = '13:25'
            df_raw.loc[i+5,'time'] = '13:30'
            modify_count = modify_count + 1

    del_command = 'drop table if exists %s;'%input_table_name
    try:
        db_handle.cursor.execute(del_command)
        db_handle.db.commit()
    except Exception as e:
        print(e)
        db_handle.db.rollback()

    output_table_name = input_table_name
    db_handle.create_table_if_not_exists(output_table_name, table_schema)
    db_handle.write_dataframe_to_mysql(df_raw, table_columns, output_table_name)

    print('modify %d in table %s'%(modify_count, input_table_name))
    '''
    other_table_name = '_'.join([prefix, '5minute_train', sf])
    del_command = 'drop table if exists %s;'%other_table_name
    try:
        db_handle.cursor.execute(del_command)
        db_handle.db.commit()
    except Exception as e:
        print(e)
        db_handle.db.rollback()
