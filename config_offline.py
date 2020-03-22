import os
import torch

conf = dict()

conf['pwd'] = os.getcwd()
conf['dataset_dir'] = conf['pwd'] + '/dataset'
conf['predictor_dir'] = conf['pwd'] + '/predictor'

conf['w1'] = 1.5
conf['w2'] = 0.15

conf['ensemble'] = 5
conf['eval_step'] = 50

conf['batchsize'] = 32
conf['max_iter'] = 100

conf['device'] = 'cpu' if torch.cuda.is_available() else 'cpu'
conf['parallel'] = 5

conf['COUNT_5MIN'] = 48
conf['INTERCEPT_5MIN'] = 40

conf['TRADE_COST_PRE'] = 0.025 # percent
conf['TRADE_COST_POST'] = 0.125 # percent

conf['hold_count'] = 1
conf['trade_stay_ratio'] = 0.0

conf['sample_ratio'] = 0.4

conf['market_name'] = '399001'
conf['stock_list'] = [ '600551', '600988', '600030', '601566', '000002', '300315', '000088', '600023',\
                       '002563', '600036', '000651', '601857', '600674', '601318', '002271', '600508',\
                       '300182', '002013', '000776', '002078', '601211', '000568', '600759', '600816',\
                       '600519', '601677', '600196', '600373', '002138', '002032', '600879', '000989',\
                       '600886', '601088', '601633', '002128', '002223', '000488', '002081', '600276',\
                       '601166', '600808', '600356', '000895', '600028', '000625', '600079', '000858',\
                       '600372', '600019', '603108', '000688', '600563', '000333', '601336', '000999',\
                       '600066', '601000', '001979', '600750', '002372', '600073', '002763', '603328',\
                       '000898', '600340', '600717', '002065', '603288', '002230', '601939', '002551' ]

conf['sql_chunk'] = 128

conf['db_address'] = 'localhost'
conf['username'] = 'root'
conf['password'] = '123'

conf['default_start_date'] = '20050101'
conf['default_end_date'] = '21050101'

conf['table_columns'] = dict()
conf['table_schema'] = dict()

conf['table_columns']['daily_raw'] = [ 'date', 'open', 'high', 'low', 'price',
                                       'ma5', 'ma10', 'ma20', 'ma60',
                                       'volume', 'vma5', 'vma20', 'cash_dividend', 'stock_dividend' ]

conf['table_schema']['daily_raw'] = '( date VARCHAR(10) NOT NULL, \
                                       open FLOAT NOT NULL, \
                                       high FLOAT NOT NULL, \
                                       low FLOAT NOT NULL, \
                                       price FLOAT NOT NULL, \
                                       ma5 FLOAT NOT NULL, \
                                       ma10 FLOAT NOT NULL, \
                                       ma20 FLOAT NOT NULL, \
                                       ma60 FLOAT NOT NULL, \
                                       volume FLOAT NOT NULL, \
                                       vma5 FLOAT NOT NULL, \
                                       vma20 FLOAT NOT NULL, \
                                       cash_dividend FLOAT NOT NULL, \
                                       stock_dividend FLOAT NOT NULL, \
                                       INDEX(date) )'

conf['table_columns']['daily_train'] = [ 'date', 'tomorrow_change', 'volume_change',
                                         'change_1', 'change_2', 'change_3',
                                         'ma5', 'ma10', 'ma20', 'ma60',
                                         'v_change_1', 'vma5', 'vma20' ]

conf['table_schema']['daily_train'] = '( date VARCHAR(10) NOT NULL, \
                                         tomorrow_change FLOAT NOT NULL, \
                                         volume_change FLOAT NOT NULL, \
                                         change_1 FLOAT NOT NULL, \
                                         change_2 FLOAT NOT NULL, \
                                         change_3 FLOAT NOT NULL, \
                                         ma5 FLOAT NOT NULL, \
                                         ma10 FLOAT NOT NULL, \
                                         ma20 FLOAT NOT NULL, \
                                         ma60 FLOAT NOT NULL, \
                                         v_change_1 FLOAT NOT NULL, \
                                         vma5 FLOAT NOT NULL, \
                                         vma20 FLOAT NOT NULL, \
                                         INDEX(date) )'

conf['table_columns']['5minute_raw'] = [ 'date', 'time', 'open', 'high', 'low', 'price', 'volume' ]

conf['table_schema']['5minute_raw'] = '( date VARCHAR(10) NOT NULL, \
                                         time VARCHAR(10) NOT NULL, \
                                         open FLOAT NOT NULL, \
                                         high FLOAT NOT NULL, \
                                         low FLOAT NOT NULL, \
                                         price FLOAT NOT NULL, \
                                         volume FLOAT NOT NULL, \
                                         INDEX(date) )'

conf['table_columns']['5minute_train'] = [ 'date', 'price_change', 'relative_volume' ]

conf['table_schema']['5minute_train'] = '( date VARCHAR(10) NOT NULL, \
                                           price_change VARCHAR(1000) NOT NULL, \
                                           relative_volume VARCHAR(1000) NOT NULL, \
                                           INDEX(date) )'
