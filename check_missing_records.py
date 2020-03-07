import time
import pandas as pd

suffix = '_5minute_raw.csv'
index = '399001'
fname = index + suffix
df = pd.read_csv(fname)

date_set = set()
i = 0

while i < len(df):
    if len(df.iloc[i]['date'].split(':')) == 2 :
        struct_time = time.strptime(df.iloc[i]['date'],"%Y/%m/%d %H:%M")
    else :
        struct_time = time.strptime(df.iloc[i]['date'],"%Y/%m/%d %H:%M:%S")
    # date_time = time.strftime('%Y%m%d', struct_time)
    date_set.add(struct_time)
    i = i + 48

date_set = list(date_set)
date_set.sort()

for i in range(0, len(date_set)-1):
    if date_set[i+1][6] == 0: # tm_wdays
        if (date_set[i+1][7] - date_set[i][7])>3: # tm_ydays
            print(time.strftime('%Y%m%d', date_set[i+1]))
    elif (date_set[i+1][7] - date_set[i][7])>1:
        print(time.strftime('%Y%m%d', date_set[i+1]))

stock_list = [ '600551', '600988', '600030', '601566', '000002', '300315', '000088', '600023', \
               '002563', '600036', '000651', '601857', '600674', '601318', '002271', '600508', \
               '300182', '002013', '000776', '002078', '601211', '000568', '600759', '600816', \
               '600519', '601677', '600196', '600373', '002138', '002032', '600879', '000989', \
               '600886', '601088', '601633', '002128', '002223', '000488', '002081', '600276', \
               '601166', '600808', '600356', '000895', '600028', '000625', '600079', '000858', \
               '600372', '600019', '603108', '000688', '600563', '000333', '601336', '000999', \
               '600066', '601000', '001979', '600750', '002372', '600073', '002763', '603328', \
               '000898', '600340', '600717', '002065', '603288', '002230', '601939', '002551' ]

vacant_count = dict()

for stock in stock_list:
    fname = stock + suffix
    df = pd.read_csv(fname)
    date_set_stock = set()
    i = 0
    while i < len(df):
        if len(df.iloc[i]['date'].split(':')) == 2 :
            struct_time = time.strptime(df.iloc[i]['date'],"%Y/%m/%d %H:%M")
        else :
            struct_time = time.strptime(df.iloc[i]['date'],"%Y/%m/%d %H:%M:%S")
        date_set_stock.add(struct_time)
        i = i + 48
    
    vacant_list = []
    last_state = True
    start_date, end_date = date_set[0], date_set[0]

    for date in date_set:
        if date in date_set_stock:
            if last_state == False:
                if start_date == end_date:
                    date_str = time.strftime('%Y%m%d', start_date)
                else :
                    date_str = time.strftime('%Y%m%d', start_date) +' - '+ time.strftime('%Y%m%d', end_date)
                vacant_list.append(date_str)
            last_state = True
        if date not in date_set_stock:
            if last_state == True:
                start_date, end_date = date, date
            else :
                end_date = date
            last_state = False
            date_str = time.strftime('%Y%m%d', date)
            if date_str not in vacant_count:
                vacant_count[date_str] = 0
            vacant_count[date_str] = vacant_count[date_str] + 1

    print stock
    print vacant_list

sorted_key = list(vacant_count.keys())
sorted_key.sort()
for key in sorted_key:
    value = vacant_count[key]
    if value >= 5:
        print key, value
