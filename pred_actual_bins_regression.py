import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

src_name = '../Stock_Offline/predictor/mlp_5min_among_stock_all_encoding_concat_later_fixed_autoencoder_20200701040019/results/pred_actual_ensemble'
x_list, y_list = [], []
ensemble = 8

with open(src_name, 'r') as f:
    line = f.readline()
    count = 0
    
    while line:
        if count >= 155000 and count < 190000:
            x = float(line.split(',')[2])/ensemble
            y = float(line.split(',')[3])
            x_list.append(x)
            y_list.append(y)
        line = f.readline()
        count = count + 1

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
    if len(value) >= 35:
        x_bins.append([float(key)])
        y_bins.append([sum(value)/len(value)])
'''
xy_list = [(x_list[i], y_list[i]) for i in range(0, len(x_list))]
xy_list_sorted = sorted(xy_list, key=lambda x:x[0], reverse=True)
x_bins, y_bins = [], []

for i in range(0, 100):
    start = int(len(xy_list_sorted)*i/100)
    end = int(len(xy_list_sorted)*(i+1)/100)
    preds = [xy[0] for xy in xy_list_sorted[start:end]]
    actuals = [xy[1] for xy in xy_list_sorted[start:end]]
    key = '%.2f'%(sum(preds)/len(preds))
    value = sum(actuals)/len(actuals)
    x_bins.append([float(key)])
    y_bins.append([value])
'''
reg = LinearRegression()
reg.fit(x_bins, y_bins)
p = reg.predict(x_bins)

plt.figure(figsize=(16, 8))
plt.scatter(x_bins, y_bins, c='blue')
plt.plot(x_bins, p, c='gray', linewidth=2)
#plt.title()
plt.show()

print(reg.coef_[0])
print(reg.intercept_)
