import os
from common_utils import log_change_single
from sklearn.linear_model import LinearRegression


class Pred_Info(object):
    def __init__(self, stock, pred, actual, flag):
        self.stock = stock
        self.pred = pred
        self.actual = actual
        self.flag = flag

    def __str__(self):
        string = '%s, %.4f, %.4f, %d'%(self.stock, self.pred, self.actual, self.flag)
        return string

class Day_Pred(object):
    def __init__(self, date, stocks, preds, actuals, flags):
        self.date = date
        self.pred_infos = dict()
        self.pred_sort_infos = dict()
        for i in range(0, len(stocks)):
            stock = stocks[i]
            pred = preds[i]
            actual = actuals[i]
            flag = flags[i]
            pred_info = Pred_Info(stock, pred, actual, flag)
            self.pred_infos[stock] = pred_info
            if flag == 0:
                self.pred_sort_infos[stock] = pred_info
        self.sort_preds()

    def sort_preds(self):
        self.sorted_stocks = sorted(self.pred_sort_infos.values(), key=lambda x:x.pred, reverse=True)
        return

def update_recent_coef(preds):
    x_list, y_list = [], []
    for d_pred in preds:
        for stock in d_pred.pred_infos:
            p_info = d_pred.pred_infos[stock]
            x = p_info.pred/ensemble
            y = p_info.actual
            x_list.append(x)
            y_list.append(y)

    xy_dict = dict()
    for i in range(0, len(x_list)):
        key = '%.2f'%x_list[i]
        value = y_list[i]
        if key not in xy_dict:
            xy_dict[key] = []
        xy_dict[key].append(value)

    x_bins, y_bins = [], []
    for key in xy_dict.keys():
        value = xy_dict[key]
        if len(value) >= len(x_list)/1000:
            x_bins.append([float(key)])
            y_bins.append([sum(value)/len(value)])

    reg = LinearRegression()
    reg.fit(x_bins, y_bins)
    return reg.coef_[0]


f_dir = '/home/zhu/workspace/Stock_Offline/predictor'
folder = 'mlp_5min_among_stock_all_encoding_concat_later_fixed_autoencoder_20200722033034'
f_name = folder + '/results/pred_actual_ensemble'

f_path = os.path.join(f_dir, f_name)

pred_list = []

with open(f_path, 'r') as f:
    line = f.readline()
    today = ''
    stocks, preds, actuals, flags = [], [], [], []

    while line:
        segments = line.split(',')
        date = segments[0]
        stock = segments[1]
        pred = float(segments[2])
        actual = float(segments[3])
        flag = int(segments[4])
        #if flag != 0:
        #    line = f.readline()
        #    continue

        if ('' == today) or (date == today):
            stocks.append(stock)
            preds.append(pred)
            actuals.append(actual)
            flags.append(flag)
        else:
            day_pred = Day_Pred(today, stocks, preds, actuals, flags)
            pred_list.append(day_pred)
            stocks = [stock]
            preds = [pred]
            actuals = [actual]
            flags = [flag]

        today = date
        line = f.readline()

day_pred = Day_Pred(today, stocks, preds, actuals, flags)
pred_list.append(day_pred)
'''
for pd in pred_list:
    print(pd.date, len(pd.pred_infos))
'''

top1_actuals, top3_actuals, top5_actuals, top10_actuals = [], [], [], []
top1_tp_days, top1_np_days, top3_tp_days, top3_np_days, top10_tp_days, top10_np_days = 0, 0, 0, 0, 0, 0
net_change_topn_stay30 = 1.0
net_change_topn_stay0 = 1.0
last_set = dict()
cash = 1.0
count = 2
cost = 0.15

coef_lower = 0.02
coef_upper = 0.20
coef = (coef_lower+coef_upper)/2
ensemble = 8

start_index = len(pred_list) - 587

for i in range(start_index-50, len(pred_list)):
    if i % 50 == 0:
        recent_preds = pred_list[i-500:i]
        coef = update_recent_coef(recent_preds)
        print('coef: %.4f'%coef)
    stay_buffer = ensemble * 0.18 / coef

    pred_info = pred_list[i]
    top1_actual = [ log_change_single(item.actual) for item in pred_info.sorted_stocks[:1] ]
    top3_actual = [ log_change_single(item.actual) for item in pred_info.sorted_stocks[:3] ]
    top5_actual = [ log_change_single(item.actual) for item in pred_info.sorted_stocks[:5] ]
    top10_actual = [ log_change_single(item.actual) for item in pred_info.sorted_stocks[:10] ]
    if i >= start_index:
        top1_actuals.extend(top1_actual)
        top3_actuals.extend(top3_actual)
        top5_actuals.extend(top5_actual)
        top10_actuals.extend(top10_actual)
        
        for item in pred_info.sorted_stocks[:1]:
            if item.actual >= 0 :
                top1_tp_days = top1_tp_days + 1
            else :
                top1_np_days = top1_np_days + 1
        for item in pred_info.sorted_stocks[:3]:
            if item.actual >= 0 :
                top3_tp_days = top3_tp_days + 1
            else :
                top3_np_days = top3_np_days + 1
        for item in pred_info.sorted_stocks[:10]:
            if item.actual >= 0 :
                top10_tp_days = top10_tp_days + 1
            else :
                top10_np_days = top10_np_days + 1

    topn_actual = [ item.actual for item in pred_info.sorted_stocks[:count] ]
    change = sum(topn_actual)/len(topn_actual)
    net_change_topn_stay0 = net_change_topn_stay0 * ( 1 + change/100 )

    candidates = [ item.stock for item in pred_info.sorted_stocks[:count] ]
    changable_stocks = last_set.keys() & pred_info.pred_infos.keys()
    changable_sorted = sorted(changable_stocks, key=lambda x:pred_info.pred_infos[x].pred, reverse=True)

    j = 0
    sellout_stocks = set()
    for j in range(0, min(len(changable_sorted), count)):
        cands_pred = pred_info.pred_infos[candidates[j]].pred
        last_set_pred = pred_info.pred_infos[changable_sorted[-1]].pred
        #print(cands_pred, last_set_pred)
        if cands_pred - last_set_pred >= stay_buffer:
            sellout_stocks.add(changable_sorted.pop())
            if len(changable_sorted) == 0:
                break
        else:
            break

    last_set_keys = set(last_set.keys())

    for stock in last_set_keys:
        if stock not in pred_info.pred_infos:
            #print(pred_info.date, stock, 'suspension')
            continue
        if stock in sellout_stocks:
            cash = cash + last_set.pop(stock)
        else :
            change = pred_info.pred_infos[stock].actual
            last_set[stock] = last_set[stock] * ( 1 + change/100 )
            #if pred_info.pred_infos[stock].flag == 1:
            #    print(pred_info.date, stock, 'limit-up')
            #if pred_info.pred_infos[stock].flag == -1:
            #    print(pred_info.date, stock, 'limit-down')

    if len(last_set) < count:
        cash_unit = cash / (count-len(last_set))
    else :
        cash_unit = 0

    for item in pred_info.sorted_stocks:
        stock = item.stock
        if len(last_set) == count:
            break
        if stock not in last_set:
            change = pred_info.pred_infos[stock].actual
            asset = cash_unit * ( 1 + change/100 ) * (1 - cost/100)
            last_set[stock] = asset
    cash = 0.0

    if i == start_index:
        base_net = sum(last_set.values())
    
    infos = []
    for key in last_set:
        info = '%s:%.6f'%(key, last_set[key])
        infos.append(info)
    infos_str = ', '.join(infos)
    #print(pred_info.date, infos_str)  #
    '''
    if i < 2460:
        for item in pred_info.sorted_stocks:
            print(item)
        print(last_set)
    '''

print(folder)

print('top1 tp/np: %.4f'%(top1_tp_days/top1_np_days))
print('top3 tp/np: %.4f'%(top3_tp_days/top3_np_days))
print('top10 tp/np: %.4f'%(top10_tp_days/top10_np_days))

# may sightly different with train output because the last 62-th step is not full of 50 smaples
print('top1 avg: %.4f'%(sum(top1_actuals)/len(top1_actuals)))
print('top3 avg: %.4f'%(sum(top3_actuals)/len(top3_actuals)))
print('top5 avg: %.4f'%(sum(top5_actuals)/len(top5_actuals)))
print('top10 avg: %.4f'%(sum(top10_actuals)/len(top10_actuals)))

final_net = sum(last_set.values())
#print('net_change_topn_stay0 %.4f'%net_change_topn_stay0)
print('net_change_top%d_optimized_cost %.4f'%(count, final_net/base_net))
