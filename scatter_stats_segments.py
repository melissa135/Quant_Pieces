import random
import pandas as pd
from common_utils import *

fname = '/home/zhu/workspace/Stock_Offline/pred_actual_ensemble'
fname_bins = '/home/zhu/workspace/Stock_Offline/pred_actual_ensemble_bins'
fname_bins_log = '/home/zhu/workspace/Stock_Offline/pred_actual_ensemble_bins_log'

df = pd.read_csv(fname)
fb = open(fname_bins, 'w')
fb_log = open(fname_bins_log, 'w')

pairs = []

for i in range(10000, len(df)):
    pred = df.iloc[i]['pred']
    actual = df.iloc[i]['actual']
    pairs.append((pred, actual))

sorted_pair = sorted(pairs, key = lambda x:x[0], reverse=True)
seg_indices = [int(i*len(sorted_pair)/100) for i in range(0,100+1)]

for i in range(0,100):
    begin, end = seg_indices[i], seg_indices[i+1]
    segs = sorted_pair[begin:end]
    avg_pred = sum(seg[0] for seg in segs)/(end-begin)
    avg_actual = sum(seg[1] for seg in segs)/(end-begin)
    log_sum = sum(log_change_single(seg[1]) for seg in segs)/(end-begin)
    avg_actual_log = log_change_single_reverse(log_sum)
    
    print(avg_pred, avg_actual, avg_actual_log)
    fb.write('%s,%s\n'%(avg_pred,avg_actual))
    fb_log.write('%s,%s\n'%(avg_pred,avg_actual_log))

fb.close()
fb_log.close()
