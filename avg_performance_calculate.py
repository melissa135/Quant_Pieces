days_count_20 = 'top1_tp_days: 495, top1_np_days: 505, top3_tp_days: 1521, top3_np_days: 1479, top10_tp_days: 5023, top10_np_days: 4975'
days_count_50 = 'top1_tp_days: 1313, top1_np_days: 1187, top3_tp_days: 3951, top3_np_days: 3549, top10_tp_days: 12812, top10_np_days: 12186'
days_count_62 = 'top1_tp_days: 1630, top1_np_days: 1457, top3_tp_days: 4872, top3_np_days: 4389, top10_tp_days: 15822, top10_np_days: 15046'

performance_step20_str = 'top1_log_avg: 0.3002, top3_log_avg: 0.3603, top10_log_avg: 0.2597'
performance_step50_str = 'top1_log_avg: 0.4486, top3_log_avg: 0.3960, top10_log_avg: 0.2677'
performance_step62_str = 'top1_log_avg: 0.4139, top3_log_avg: 0.3745, top10_log_avg: 0.2541'

net_asset_20 = 'top5_stay30_no_cost: 12.2946, top5_stay30_normal_cost: 6.0605, top2_stay30_normal_cost: 6.6839, top1_stay30_normal_cost: 13.6146'
net_asset_50 = 'top5_stay30_no_cost: 458.7838, top5_stay30_normal_cost: 87.7550, top2_stay30_normal_cost: 154.5673, top1_stay30_normal_cost: 812.6891'
net_asset_62 = 'top5_stay30_no_cost: 1903.2105, top5_stay30_normal_cost: 250.1459, top2_stay30_normal_cost: 403.1513, top1_stay30_normal_cost: 2228.2731'

tpd_1_20 = int(days_count_20.split(',')[0].split(':')[1])
npd_1_20 = int(days_count_20.split(',')[1].split(':')[1])
tpd_3_20 = int(days_count_20.split(',')[2].split(':')[1])
npd_3_20 = int(days_count_20.split(',')[3].split(':')[1])
tpd_10_20 = int(days_count_20.split(',')[4].split(':')[1])
npd_10_20 = int(days_count_20.split(',')[5].split(':')[1])

tpd_1_62 = int(days_count_62.split(',')[0].split(':')[1])
npd_1_62 = int(days_count_62.split(',')[1].split(':')[1])
tpd_3_62 = int(days_count_62.split(',')[2].split(':')[1])
npd_3_62 = int(days_count_62.split(',')[3].split(':')[1])
tpd_10_62 = int(days_count_62.split(',')[4].split(':')[1])
npd_10_62 = int(days_count_62.split(',')[5].split(':')[1])

tn_1_ratio = (tpd_1_62 - tpd_1_20) / ( npd_1_62 - npd_1_20 )
tn_3_ratio = (tpd_3_62 - tpd_3_20) / ( npd_3_62 - npd_3_20 )
tn_10_ratio = (tpd_10_62 - tpd_10_20) / ( npd_10_62 - npd_10_20 )

performance_step20_list = [ float(segment.split(':')[1]) for segment in performance_step20_str.split(',') ]
performance_step62_list = [ float(segment.split(':')[1]) for segment in performance_step62_str.split(',') ]

top5_stay30_no_cost_20 = float(net_asset_20.split(',')[0].split(':')[1])
top5_stay30_normal_cost_20 = float(net_asset_20.split(',')[1].split(':')[1])
top2_stay30_normal_cost_20 = float(net_asset_20.split(',')[2].split(':')[1])
top1_stay30_normal_cost_20 = float(net_asset_20.split(',')[3].split(':')[1])

top5_stay30_no_cost_50 = float(net_asset_50.split(',')[0].split(':')[1])
top5_stay30_normal_cost_50 = float(net_asset_50.split(',')[1].split(':')[1])
top2_stay30_normal_cost_50 = float(net_asset_50.split(',')[2].split(':')[1])
top1_stay30_normal_cost_50 = float(net_asset_50.split(',')[3].split(':')[1])

A = 20
B = 42

performance = []
for i in range(0, 3):
    score = (performance_step62_list[i] * (A+B) - performance_step20_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus, 20 - 62')
print('%.4f,'%tn_1_ratio, '%.4f,'%tn_3_ratio, '%.4f,'%tn_10_ratio)
#print('%.4f'%sum(performance))
print(', '.join([ '%.4f' % p for p in performance]))
print('net change of top1_stay30_normal_cost: %.4f'%(top1_stay30_normal_cost_50/top1_stay30_normal_cost_20))
print('net change of top2_stay30_normal_cost: %.4f'%(top2_stay30_normal_cost_50/top2_stay30_normal_cost_20))
print('net change of top5_stay30_normal_cost: %.4f'%(top5_stay30_normal_cost_50/top5_stay30_normal_cost_20))
print('net change of top5_stay30_no_cost: %.4f'%(top5_stay30_no_cost_50/top5_stay30_no_cost_20))

# ----------------------------------------------------------------------------------------

tpd_1_50 = int(days_count_50.split(',')[0].split(':')[1])
npd_1_50 = int(days_count_50.split(',')[1].split(':')[1])
tpd_3_50 = int(days_count_50.split(',')[2].split(':')[1])
npd_3_50 = int(days_count_50.split(',')[3].split(':')[1])
tpd_10_50 = int(days_count_50.split(',')[4].split(':')[1])
npd_10_50 = int(days_count_50.split(',')[5].split(':')[1])

tpd_1_62 = int(days_count_62.split(',')[0].split(':')[1])
npd_1_62 = int(days_count_62.split(',')[1].split(':')[1])
tpd_3_62 = int(days_count_62.split(',')[2].split(':')[1])
npd_3_62 = int(days_count_62.split(',')[3].split(':')[1])
tpd_10_62 = int(days_count_62.split(',')[4].split(':')[1])
npd_10_62 = int(days_count_62.split(',')[5].split(':')[1])

tn_1_ratio = (tpd_1_62 - tpd_1_50) / ( npd_1_62 - npd_1_50 )
tn_3_ratio = (tpd_3_62 - tpd_3_50) / ( npd_3_62 - npd_3_50 )
tn_10_ratio = (tpd_10_62 - tpd_10_50) / ( npd_10_62 - npd_10_50 )

performance_step50_list = [ float(segment.split(':')[1]) for segment in performance_step50_str.split(',') ]
performance_step62_list = [ float(segment.split(':')[1]) for segment in performance_step62_str.split(',') ]

top5_stay30_no_cost_62 = float(net_asset_62.split(',')[0].split(':')[1])
top5_stay30_normal_cost_62 = float(net_asset_62.split(',')[1].split(':')[1])
top2_stay30_normal_cost_62 = float(net_asset_62.split(',')[2].split(':')[1])
top1_stay30_normal_cost_62 = float(net_asset_62.split(',')[3].split(':')[1])

A = 50
B = 12

performance = []
for i in range(0, 3):
    score = (performance_step62_list[i] * (A+B) - performance_step50_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus, 50 - 62')
print('%.4f,'%tn_1_ratio, '%.4f,'%tn_3_ratio, '%.4f,'%tn_10_ratio)
#print('%.4f'%sum(performance))
print(', '.join([ '%.4f' % p for p in performance]))
print('net change of top1_stay30_normal_cost: %.4f'%(top1_stay30_normal_cost_62/top1_stay30_normal_cost_50))
print('net change of top2_stay30_normal_cost: %.4f'%(top2_stay30_normal_cost_62/top2_stay30_normal_cost_50))
print('net change of top5_stay30_normal_cost: %.4f'%(top5_stay30_normal_cost_62/top5_stay30_normal_cost_50))
print('net change of top5_stay30_no_cost: %.4f'%(top5_stay30_no_cost_62/top5_stay30_no_cost_50))
'''
47 - 57
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
124
1.3347
0.3473, 0.2317, 0.2595, 0.2560, 0.2401
>>> 
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
190
1.5455
0.3754, 0.4076, 0.1937, 0.2656, 0.3032
>>> 
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
178
1.4940
0.4086, 0.3711, 0.2837, 0.1783, 0.2522
>>> 
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
162
1.5563
0.3282, 0.4154, 0.3774, 0.2010, 0.2343
>>> 
'''

'''
47 - 57
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
170
1.6138
0.3991, 0.4054, 0.3645, 0.1592, 0.2855
>>> 
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
180
1.6056
0.5311, 0.2132, 0.3136, 0.3538, 0.1939
>>> 
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
90
1.2774
0.4585, 0.2980, 0.2380, 0.2129, 0.0700
>>> 
=== RESTART: /home/zhu/workspace/Quant_Pieces/avg_performance_calculate.py ===
normal, random test A
114
1.2225
0.3164, 0.3261, 0.1507, 0.2813, 0.1481
>>> 

'''
