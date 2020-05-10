import random
import pandas as pd

fname = '/home/zhu/workspace/Stock_Offline/pred_actual_ensemble'
fname_sample = '/home/zhu/workspace/Stock_Offline/pred_actual_ensemble_sample'
fname_bins = '/home/zhu/workspace/Stock_Offline/pred_actual_ensemble_bins'

df = pd.read_csv(fname)
fs = open(fname_sample, 'w')
fb = open(fname_bins, 'w')

bins = dict()

for i in range(0, len(df)):
    pred = df.iloc[i]['pred']
    actual = df.iloc[i]['actual']
    pred_str = str(int(pred)) # '%.1f'%pred
    if pred_str not in bins.keys():
        bins[pred_str] = []
    bins[pred_str].append(actual)
    if random.random() < 0.01 :
        fs.write(pred_str+','+str(actual)+'\n')

keys = [float(k) for k in bins.keys()]
keys.sort()
keys = [str(int(k)) for k in keys ] # '%.1f'%k

for k in keys:
    avg = sum(bins[k])/len(bins[k])
    print(k, avg, len(bins[k]))
    if len(bins[k]) >= 100:
        fb.write(k+','+str(avg)+'\n')

fs.close()
fb.close()
