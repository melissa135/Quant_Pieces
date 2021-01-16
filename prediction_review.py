import os
from common_utils import log_change_single
from sklearn.linear_model import LinearRegression


class Pred_Info(object):
    
    def __init__(self, stock, pred, target, actual, flag):
        self.stock = stock
        self.pred = pred
        self.target = target
        self.actual = actual
        self.flag = flag

    def __str__(self):
        string = '%s, %.4f, %.4f, %.4f, %d' % (self.stock, self.pred, self.target, self.actual, self.flag)
        return string


class Day_Pred_Infos(object):
    
    def __init__(self, date, stocks, preds, targets, actuals, flags):
        self.date = date
        self.all_stock_info = dict()
        self.sorted_stock_id = list()
        self.limit_up_down = list()
        tmp_pair = list()  # only tradable stock, pred
        
        for i in range(0, len(stocks)):
            stock = stocks[i]
            pred = preds[i]
            target = targets[i]
            actual = actuals[i]
            flag = flags[i]
            pred_info = Pred_Info(stock, pred, target, actual, flag)
            
            self.all_stock_info[stock] = pred_info
            if flag == 0:
                tmp_pair.append((stock, pred))
            else:
                self.limit_up_down.append(stock)

        self.sorted_stock_id = [item[0] for item in sorted(tmp_pair, key=lambda x:x[1], reverse=True)]


def calc_pa_product(a_list, p_list):
    sum_a = sum(a_list)
    sum_p = sum(p_list)
    n = len(a_list)
    sum_pa = sum([a_list[i]*p_list[i] for i in range(0, n)])
    pa_product = 2*(n*sum_pa - sum_a*sum_p)
    return pa_product


f_dir = '/home/zhu/workspace/Stock_Offline/predictor'
folder = 'mlp_dec2020_baseline_20210116131932'
f_name = folder + '/results/pred_actual_ensemble'

f_path = os.path.join(f_dir, f_name)

all_day_infos = []

with open(f_path, 'r') as f:
    
    line = f.readline()
    today = ''
    stocks, preds, targets, actuals, flags = [], [], [], [], []

    while line:
        segments = line.split(',')
        date = segments[0]
        stock = segments[1]
        pred = float(segments[2])
        target = float(segments[3])
        actual = float(segments[4])
        flag = int(segments[5])
        
        if ('' == today) or (date == today):
            stocks.append(stock)
            preds.append(pred)
            targets.append(target)
            actuals.append(actual)
            flags.append(flag)
        else:
            day_info = Day_Pred_Infos(today, stocks, preds, targets, actuals, flags)
            all_day_infos.append(day_info)
            stocks = [stock]
            preds = [pred]
            targets = [target]
            actuals = [actual]
            flags = [flag]

        today = date
        line = f.readline()

day_info = Day_Pred_Infos(today, stocks, preds, targets, actuals, flags)
all_day_infos.append(day_info)
'''
for pd in pred_list:
    print(pd.date, len(pd.pred_infos))
'''

top1_actuals, top3_actuals, top10_actuals, topfront_actuals = [], [], [], []
top1_tp_days, top1_np_days, top3_tp_days, top3_np_days, top10_tp_days, top10_np_days = 0, 0, 0, 0, 0, 0
topfront_tp_days, topfront_np_days = 0, 0
net_change_topn_stay30 = 1.0
total_hold, total_trade = 0, 0
limit_up_num, limit_down_num = 0, 0
limit_influence = 0.0
pa_product_list = []
hold_order_list = []

cash = 1.0
count = 5
cost = 0.0  # 0.15

coef = 0.5
ensemble = 8

last_set = dict()
'''
last_set['002065'] = 164.6670749097408
last_set['000651'] = 156.33101487337103
last_set['000002'] = 157.84421136539086
last_set['600816'] = 157.9002796510637
last_set['603108'] = 158.88067754944214
cash = 0.0
'''
base_net = sum(last_set.values()) + cash
last_order_dict = dict()

start_index = len(all_day_infos) - 750
end_index = len(all_day_infos)

for i in range(start_index, end_index):

    day_infos = all_day_infos[i]
    front_range = int(0.3*len(day_infos.sorted_stock_id))

    avg_actuals = sum([day_infos.all_stock_info[sid].actual for sid in day_infos.sorted_stock_id])/len(day_infos.sorted_stock_id)
    log_avg_actuals = log_change_single(avg_actuals)
    
    top1_sids = day_infos.sorted_stock_id[:1] +\
                [sid for sid in day_infos.limit_up_down if last_order_dict.get(sid, 72) <= 1]
    top1_actual = [log_change_single(day_infos.all_stock_info[sid].actual) - log_avg_actuals for sid in top1_sids]
    top3_sids = day_infos.sorted_stock_id[:3] +\
                [sid for sid in day_infos.limit_up_down if last_order_dict.get(sid, 72) <= 3]
    top3_actual = [log_change_single(day_infos.all_stock_info[sid].actual) - log_avg_actuals for sid in top3_sids]
    top10_sids = day_infos.sorted_stock_id[:10] +\
                 [sid for sid in day_infos.limit_up_down if last_order_dict.get(sid, 72) <= 10]
    top10_actual = [log_change_single(day_infos.all_stock_info[sid].actual) - log_avg_actuals for sid in top10_sids]
    topfront_sids = day_infos.sorted_stock_id[:front_range] +\
                    [sid for sid in day_infos.limit_up_down if last_order_dict.get(sid, 72) <= front_range]
    topfront_actual = [log_change_single(day_infos.all_stock_info[sid].actual) - log_avg_actuals for sid in topfront_sids]
        
    top1_actuals.extend(top1_actual)
    top3_actuals.extend(top3_actual)
    top10_actuals.extend(top10_actual)
    topfront_actuals.extend(topfront_actual)
        
    for sid in top1_sids:
        if day_infos.all_stock_info[sid].actual - avg_actuals >= 0 :
            top1_tp_days = top1_tp_days + 1
        else :
            top1_np_days = top1_np_days + 1
    for sid in top3_sids:
        if day_infos.all_stock_info[sid].actual - avg_actuals >= 0 :
            top3_tp_days = top3_tp_days + 1
        else :
            top3_np_days = top3_np_days + 1
    for sid in top10_sids:
        if day_infos.all_stock_info[sid].actual - avg_actuals >= 0 :
            top10_tp_days = top10_tp_days + 1
        else :
            top10_np_days = top10_np_days + 1
    for sid in topfront_sids:
        if day_infos.all_stock_info[sid].actual - avg_actuals >= 0 :
            topfront_tp_days = topfront_tp_days + 1
        else :
            topfront_np_days = topfront_np_days + 1

    a_list = [ day_infos.all_stock_info[sid].actual for sid in day_infos.sorted_stock_id ]
    p_list = [ day_infos.all_stock_info[sid].pred/ensemble for sid in day_infos.sorted_stock_id ]
    pa_product = calc_pa_product(a_list, p_list)
    pa_product_list.append(pa_product)

    candidates = day_infos.sorted_stock_id[:count]
    changable_stocks = last_set.keys() & set(day_infos.sorted_stock_id)

    sellout_stocks = set()
    boundary_stock = day_infos.sorted_stock_id[front_range-1]
    boundary_pred = day_infos.all_stock_info[boundary_stock].pred

    for sid in changable_stocks:
        stock_pred = day_infos.all_stock_info[sid].pred
        if stock_pred < boundary_pred:
            sellout_stocks.add(sid)

    last_set_keys = set(last_set.keys())
    total_hold = total_hold + len(last_set_keys)
    total_trade = total_trade + len(sellout_stocks)

    for sid in last_set_keys:
        if sid in sellout_stocks:
            cash = cash + last_set.pop(sid)
        elif sid in day_infos.all_stock_info:  # include limit-up or limit-down
            change = day_infos.all_stock_info[sid].actual
            last_set[sid] = last_set[sid] * ( 1 + change/100 )
            if sid not in day_infos.sorted_stock_id:
                limit_influence = limit_influence + change/100
                if day_infos.all_stock_info[sid].flag == 1:
                    limit_up_num = limit_up_num + 1
                elif day_infos.all_stock_info[sid].flag == -1:
                    limit_down_num = limit_down_num + 1
                else:
                    print('something wrong about %s at %s'%(sid, day_infos.date))
        else:
            # 'suspension'
            continue
            
    if len(last_set) < count:
        cash_unit = cash / (count-len(last_set))
    else :
        cash_unit = 0

    for sid in day_infos.sorted_stock_id:
        if len(last_set) == count:
            break
        if sid not in last_set:
            change = day_infos.all_stock_info[sid].actual
            asset = cash_unit * ( 1 + change/100 ) * (1 - cost/100)
            last_set[sid] = asset
    
    cash = 0.0
    for j, sid in enumerate(day_infos.sorted_stock_id):
        last_order_dict[sid] = j+1  # the limit-up and limit-down stocks would be still kept
        if sid in last_set.keys():
            hold_order_list.append(j+1)
            
    # print(day_infos.date)
    # print(last_set)

print(folder)

print('top1 tp/np: %.4f'%(top1_tp_days/top1_np_days))
print('top3 tp/np: %.4f'%(top3_tp_days/top3_np_days))
print('top10 tp/np: %.4f'%(top10_tp_days/top10_np_days))
print('topfront tp/np: %.4f'%(topfront_tp_days/topfront_np_days))

# may sightly different with train output because the last 62-th step is not full of 50 smaples
print('top1 avg: %.4f'%(sum(top1_actuals)/len(top1_actuals)))
print('top3 avg: %.4f'%(sum(top3_actuals)/len(top3_actuals)))
print('top10 avg: %.4f'%(sum(top10_actuals)/len(top10_actuals)))
print('topfront avg: %.4f'%(sum(topfront_actuals)/len(topfront_actuals)))

print('avg order: %.4f'%(sum(hold_order_list)/len(hold_order_list)))
print('limit_up_num %d, limit_down_num %d'%(limit_up_num, limit_down_num))
print('limit influence: %.4f'%limit_influence)

print('pa_product avg: %.2f'%(sum(pa_product_list)/len(pa_product_list)))

final_net = sum(last_set.values())
print('trade ratio: %.4f'%(total_trade/total_hold))
print('net_change_top%d_no_cost %.4f'%(count, final_net/base_net))
