#-*- coding:utf-8 -*-
import os
import sys
import math
from database_utils import *
from config_offline import conf
from common_utils import prepare_data_uniform_qfq, get_data_uniform_qfq
from pyecharts import Bar, Grid, Line, Kline, Overlap, Scatter


CHART_DIR = '/home/zhu/workspace/Quant_Pieces/'


def max_accumul_change_with_decay(changes):
    extend_range = 10
    decay_coef = 0.8
    max_changes = []

    for i in range(0, len(changes) - extend_range):
        current_decay = decay_coef
        max_change = changes[i] * (current_decay + 0.2)
        current_accumul = max_change
        for j in range(i + 1, i + extend_range):
            current_accumul = current_accumul + changes[j] * (current_decay + 0.2)
            current_decay = current_decay * decay_coef
            max_change = max(max_change, current_accumul)
        max_changes.append(max_change)

    avg = sum(max_changes)/len(max_changes)
    max_changes = [item - avg for item in max_changes]
    max_changes.extend([0] for i in range(0, extend_range))
    return max_changes


def plot_k_lines():

    stock_id_list = []
    table_name_list = []

    stock_id = '399001'
    table_name = 'market' + '_daily_raw_' + stock_id
    stock_id_list.append(stock_id)
    table_name_list.append(table_name)
    '''
    for stock_id in conf['stock_list']:
        table_name = 'stock' + conf['table_names']['daily_raw'] + stock_id
        stock_id_list.append(stock_id)
        table_name_list.append(table_name)
    '''
    columns_list = ['date', 'open', 'price', 'high', 'low', 'ma5', 'ma20', 'volume', 'cash_dividend', 'stock_dividend']

    for k in range(0, len(stock_id_list)):
        stock_id = stock_id_list[k]
        table_name = table_name_list[k]

        df_result = db_handle.read_recent_dataframe_from_mysql(columns_list, table_name, counts=121)
        df_result = prepare_data_uniform_qfq(df_result, 0, len(df_result)-1)

        dates = list(df_result['date'][1:])
        prices = [[get_data_uniform_qfq(df_result, 'open', i),
                   get_data_uniform_qfq(df_result, 'price', i),
                   get_data_uniform_qfq(df_result, 'high', i),
                   get_data_uniform_qfq(df_result, 'low', i)] for i in range(1, len(df_result))]
        ma5 = [get_data_uniform_qfq(df_result, 'ma5', i) for i in range(1, len(df_result))]
        ma20 = [get_data_uniform_qfq(df_result, 'ma20', i) for i in range(1, len(df_result))]

        tomorrow_changes = [(prices[i+1][1] - prices[i][1])/prices[i][1] for i in range(0, len(prices) - 1)] + [0]
        target_extend3days = [tomorrow_changes[i] + 0.5 * tomorrow_changes[i+1] + 0.25 * tomorrow_changes[i+2]
                              for i in range(0, len(prices) - 3)] + [0] * 3
        target_extend5days = [tomorrow_changes[i] + 0.7 * tomorrow_changes[i+1] + 0.5 * tomorrow_changes[i+2] +
                              + 0.35 * tomorrow_changes[i+3] + 0.25 * tomorrow_changes[i+4]
                              for i in range(0, len(prices) - 5)] + [0] * 5
        target_new = max_accumul_change_with_decay(tomorrow_changes)

        cds = list(df_result['cash_dividend'][1:len(df_result)-1])
        sds = list(df_result['stock_dividend'][1:len(df_result)-1])

        dividend_tuples = []
        for i in range(0, len(cds)):
            if (cds[i] != 0) or (sds[i] != 0):
                dividend_tuples.append((i, cds[i], sds[i]))

        sct = Scatter()
        idx, height = [], []
        for d_t in dividend_tuples:
            i, c, s = d_t
            dates[i] = dates[i] + '\n分红 %d 除权 %d' % (c, s)
            idx.append(i)
            height.append(0.98 * prices[i][3])
        sct.add('Dividend', idx, height)

        kline = Kline(width=1200, height=800)
        kline.add('K-line', dates, prices, is_datazoom_show=True,
                  datazoom_xaxis_index=[0, 1], xaxis_pos='top', is_xaxislabel_align=True)

        bar = Bar()
        bar.add('target', x_axis=dates, y_axis=target_new, is_legend_show=False,
                is_datazoom_show=True, is_stack=True, is_xaxislabel_align=True)

        grid = Grid(page_title='%s Daily Kline' % stock_id)
        grid.add(kline, grid_bottom='40%')
        grid.add(bar, grid_top='65%')

        line = Line()
        line.add('ma5', dates, ma5, is_datazoom_show=True, is_xaxislabel_align=True,
                 is_fill=False, line_opacity=0.8, is_smooth=True)
        line.add('ma20', dates, ma20, is_datazoom_show=True, is_xaxislabel_align=True,
                 is_fill=False, line_opacity=0.8, is_smooth=True)

        overlap = Overlap('%s target kline' % stock_id)
        overlap.add(grid)
        overlap.add(line)
        overlap.add(sct)
        target_dir = CHART_DIR + '%s_target_kline.html' % stock_id
        overlap.render(path=target_dir)
        # grid.render(path='%s_daily_kline.html' % stock_id)

    return True


if __name__ == '__main__':

    db_handle = database_utils(conf['db_address'], conf['username'], conf['password'], 'stock_dev')

    flag = plot_k_lines()

    db_handle.close()
