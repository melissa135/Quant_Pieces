import os
import torch
import network_structure
import matplotlib.pyplot as plt

change_str = '-0.6794250 0.80953413 0.68961795 0.82952016 0.92945031 0.83951318 0.42979957 0.01009294 -0.0798441 -0.5695019 -1.2690129 -0.9492364 -1.1590897 -1.2290409 -1.0191875 -1.1191177 -1.0691526 -1.2290409 -1.2590199 -1.1690828 -1.2590199 -1.3189780 -1.0391736 -0.6894180 -0.5695019 -0.5695019 -0.9192574 -1.0591596 -0.9092644 -0.8193272 -0.5695019 -0.7494761 -0.0698511 -0.4695717 -0.6394530 -0.4695717 -0.3896276 -0.2896975 -0.0698511 0.72959001 0.42979957 0.57969479 0.42979957 0.48975765 -0.0698511 -0.0698511 -0.1697813 -0.1198162'
volume_str = '2.15429243 3.75866975 4.49280642 1.35279116 4.42887879 10.2600411 2.49798937 1.77278882 1.94051293 2.63203118 3.55726334 2.66158911 2.10205049 1.73154519 1.94051293 1.89858190 1.32323322 1.29023831 2.33164005 0.56572516 2.70077056 1.39953394 1.56450847 0.84068271 4.14635990 1.09433106 2.24846539 1.71917210 1.76316531 1.93226420 0.40143802 0.89292465 3.92020731 0.97266234 1.02421688 0.86199192 1.08539494 0.64271328 1.70748640 2.14673109 2.75095032 2.00787753 0.51279583 2.23609230 1.53495054 0.96510101 1.04483870 1.18919141'

change_list = [float(item) for item in change_str.split(' ')]
volume_list = [float(item) for item in volume_str.split(' ')]

f_dir = '/home/zhu/workspace/Stock_Offline/predictor/mlp_5min_among_stocks_A'
f_path = os.path.join(f_dir, 'step_50/ae2_saved_0th.pt')
ae2 = torch.load(f_path)

input1 = torch.Tensor([change_list])
input2 = torch.Tensor([volume_list])
output, output_v = ae2(input1, input2)

recon_change_list = output[0].tolist()
recon_volume_list = output_v[0].tolist()

X = range(0,len(change_list))
figure = plt.figure(figsize=(12,8),dpi=80)

axes1 = figure.add_subplot(2,1,1)
axes1.plot(X, change_list, color='blue', linewidth=1)
axes1.bar(X, volume_list, color ='red', align='center', width=0.2)

axes2 = figure.add_subplot(2,1,2)
axes2.plot(X, recon_change_list, color='blue', linewidth=1)
axes2.bar(X, recon_volume_list, color ='red', align='center', width=0.2)

plt.show()
# figure.savefig(path_+'/vision/vision_%d.png'%i)
