import random
import pandas as pd

fname = '/home/zhu/workspace/Stock_Offline/pred_actual_5ensemble'
fname_bins = '/home/zhu/workspace/Stock_Offline/pred_actual_5ensemble_bins'

df = pd.read_csv(fname)
fb = open(fname_bins, 'w')

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
    
    print(avg_pred, avg_actual)
    fb.write('%s,%s\n'%(avg_pred,avg_actual))

fb.close()
