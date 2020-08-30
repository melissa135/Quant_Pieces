import os
import time
import pymysql
import pandas as pd
from config_offline import conf
from pandas.io.parsers import read_csv


class database_utils(object):

    def __init__(self, db_address, username, password, db_name):
        self.db = pymysql.connect(db_address, username, password, db_name)
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def create_table_if_not_exists(self, table_name, table_schema):
        sql = 'CREATE TABLE IF NOT EXISTS %s %s;'%(table_name, table_schema)
        self.cursor.execute(sql)
        return

    def get_latest_date_from_mysql(self, table_name):
        date = conf['default_start_date']
        sql = 'SELECT MAX(date) FROM %s'%table_name
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result[0] is None:
                return date
            date = result[0]
        except Exception as e:
            print(e)
        return date

    def get_latest_date_from_mysql_with_condition(self, table_name, columns, values):
        date = conf['default_start_date']
        values = [ "'%s'"%v if isinstance(v, str) else str(v) for v in values ]
        condition = ' AND '.join(columns[i]+'='+values[i] for i in range(0, len(columns)))
        sql = 'SELECT MAX(date) FROM %s WHERE %s'%(table_name, condition)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result[0] is None:
                return date
            date = result[0]
        except Exception as e:
            print(e)
        return date

    def read_dataframe_from_mysql(self, columns_list, table_name, start_date=None, end_date=None, include_start=True):
        #default: include start day, do not include end_day
        if start_date is None:
            start_date = conf['default_start_date']
        if end_date is None:
            end_date = conf['default_end_date']

        columns_str = ','.join(columns_list)
        if include_start :
            sql = 'SELECT %s from %s WHERE date >= %s AND date < %s'%(columns_str, table_name, start_date, end_date)
        else :
            sql = 'SELECT %s from %s WHERE date > %s AND date < %s'%(columns_str, table_name, start_date, end_date)

        result = []
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)

        if len(result) == 0 :
            df_result = pd.DataFrame(columns=columns_list)
            return df_result

        columns = [[ row[i] for row in result ] for i in range(0, len(result[0]))]
        data_dict = { columns_list[i]:columns[i] for i in range(0, len(columns)) }
        df_result = pd.DataFrame(data_dict)

        return df_result

    def read_recent_dataframe_from_mysql(self, columns_list, table_name, counts):

        columns_str = ','.join(columns_list)
        if counts == 0 :
            sql = 'SELECT %s FROM %s WHERE date = \
                   (SELECT MAX(date) FROM %s);'%(columns_str, table_name, table_name)
        else:
            sql = 'SELECT * FROM \
                   ( SELECT %s FROM %s ORDER BY date DESC LIMIT %d ) t0 \
                   ORDER BY date;'%(columns_str, table_name, counts)
        
        result = []
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)

        if len(result) == 0 :
            df_result = pd.DataFrame(columns=columns_list)
            return df_result

        columns = [[ row[i] for row in result ] for i in range(0, len(result[0]))]
        data_dict = { columns_list[i]:columns[i] for i in range(0, len(columns)) }
        df_result = pd.DataFrame(data_dict)

        return df_result

    def read_dataframe_from_mysql_with_condition(self, columns_list, table_name, c_columns, c_values):

        columns_str = ','.join(columns_list)
        c_values = [ "'%s'"%v if isinstance(v, str) else str(v) for v in c_values ]
        condition = ' AND '.join(c_columns[i]+'='+str(c_values[i]) for i in range(0, len(c_columns)))
        sql = 'SELECT %s FROM %s WHERE %s'%(columns_str, table_name, condition)

        result = []
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)

        if len(result) == 0 :
            df_result = pd.DataFrame(columns=columns_list)
            return df_result

        columns = [[ row[i] for row in result ] for i in range(0, len(result[0]))]
        data_dict = { columns_list[i]:columns[i] for i in range(0, len(columns)) }
        df_result = pd.DataFrame(data_dict)

        return df_result

    def write_dataframe_to_mysql(self, df, columns_list, table_name):

        values = []
        columns_str = ','.join(columns_list)

        for i in range(0, len(df)):

            row = df.iloc[i]

            value = '(' + ','.join(["'%s'"%item if isinstance(item, str) else str(item) for item in row]) + ')'
            values.append(value)

            if (len(values) == conf['sql_chunk']) or (i == len(df)-1):
                values_str = ','.join(values)
                sql = "INSERT INTO %s \
                       (%s) \
                       VALUES %s;" % (table_name, columns_str, values_str)
                values = []

                try:
                    self.cursor.execute(sql)
                    self.db.commit()
                except Exception as e:
                    print(e)
                    self.db.rollback()
        return True

    def update_mysql_data(self, table_name, condition_cols, condition_vals, columns, values):

        condition_vals = [ "'%s'"%v if isinstance(v, str) else str(v) for v in condition_vals ]
        condition = ' AND '.join(condition_cols[i]+'='+condition_vals[i] for i in range(0, len(condition_cols)))
        values = [ "'%s'"%v if isinstance(v, str) else str(v) for v in values ]
        update = ', '.join(columns[i]+'='+values[i] for i in range(0, len(columns)))

        sql = 'UPDATE %s SET %s WHERE %s'%(table_name, update, condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        return True
