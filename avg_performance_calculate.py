days_count_20 = 'top1_tp_days: 517, top1_np_days: 483, top3_tp_days: 1564, top3_np_days: 1436, top10_tp_days: 5042, top10_np_days: 4956'
days_count_50 = 'top1_tp_days: 1292, top1_np_days: 1208, top3_tp_days: 3863, top3_np_days: 3637, top10_tp_days: 12633, top10_np_days: 12365'
days_count_63 = 'top1_tp_days: 1618, top1_np_days: 1543, top3_tp_days: 4876, top3_np_days: 4607, top10_tp_days: 15940, top10_np_days: 15668'

performance_step20_str = 'top1_log_avg: 0.4238, top3_log_avg: 0.3667, top10_log_avg: 0.2538'
performance_step50_str = 'top1_log_avg: 0.3799, top3_log_avg: 0.3008, top10_log_avg: 0.2280'
performance_step63_str = 'top1_log_avg: 0.3579, top3_log_avg: 0.2978, top10_log_avg: 0.2137'

net_asset_20 = 'top5_stay30_no_cost: 24.1721, top5_stay30_normal_cost: 12.0011, top2_stay30_normal_cost: 12.1811, top5_coef_based_normal_cost: 7.9257, top2_coef_based_normal_cost: 11.5348'
net_asset_50 = 'top5_stay30_no_cost: 1280.5870, top5_stay30_normal_cost: 247.7545, top2_stay30_normal_cost: 229.3293, top5_coef_based_normal_cost: 131.3422, top2_coef_based_normal_cost: 785.5509'
net_asset_63 = 'top5_stay30_no_cost: 5550.5448, top5_stay30_normal_cost: 718.4335, top2_stay30_normal_cost: 907.3443, top5_coef_based_normal_cost: 304.7171, top2_coef_based_normal_cost: 2770.9628'

tpd_1_20 = int(days_count_20.split(',')[0].split(':')[1])
npd_1_20 = int(days_count_20.split(',')[1].split(':')[1])
tpd_3_20 = int(days_count_20.split(',')[2].split(':')[1])
npd_3_20 = int(days_count_20.split(',')[3].split(':')[1])
tpd_10_20 = int(days_count_20.split(',')[4].split(':')[1])
npd_10_20 = int(days_count_20.split(',')[5].split(':')[1])

tpd_1_63 = int(days_count_63.split(',')[0].split(':')[1])
npd_1_63 = int(days_count_63.split(',')[1].split(':')[1])
tpd_3_63 = int(days_count_63.split(',')[2].split(':')[1])
npd_3_63 = int(days_count_63.split(',')[3].split(':')[1])
tpd_10_63 = int(days_count_63.split(',')[4].split(':')[1])
npd_10_63 = int(days_count_63.split(',')[5].split(':')[1])

tn_1_ratio = (tpd_1_63 - tpd_1_20) / ( npd_1_63 - npd_1_20 )
tn_3_ratio = (tpd_3_63 - tpd_3_20) / ( npd_3_63 - npd_3_20 )
tn_10_ratio = (tpd_10_63 - tpd_10_20) / ( npd_10_63 - npd_10_20 )

performance_step20_list = [ float(segment.split(':')[1]) for segment in performance_step20_str.split(',') ]
performance_step63_list = [ float(segment.split(':')[1]) for segment in performance_step63_str.split(',') ]

top5_stay30_no_cost_20 = float(net_asset_20.split(',')[0].split(':')[1])
top5_stay30_normal_cost_20 = float(net_asset_20.split(',')[1].split(':')[1])
top2_stay30_normal_cost_20 = float(net_asset_20.split(',')[2].split(':')[1])
top5_coef_based_normal_cost_20 = float(net_asset_20.split(',')[3].split(':')[1])
top2_coef_based_normal_cost_20 = float(net_asset_20.split(',')[4].split(':')[1])

top5_stay30_no_cost_50 = float(net_asset_50.split(',')[0].split(':')[1])
top5_stay30_normal_cost_50 = float(net_asset_50.split(',')[1].split(':')[1])
top2_stay30_normal_cost_50 = float(net_asset_50.split(',')[2].split(':')[1])
top5_coef_based_normal_cost_50 = float(net_asset_50.split(',')[3].split(':')[1])
top2_coef_based_normal_cost_50 = float(net_asset_50.split(',')[4].split(':')[1])

A = 20
B = 43

performance = []
for i in range(0, 3):
    score = (performance_step63_list[i] * (A+B) - performance_step20_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus, 20 - 63')
print('%.4f,'%tn_1_ratio, '%.4f,'%tn_3_ratio, '%.4f,'%tn_10_ratio)
#print('%.4f'%sum(performance))
print(', '.join([ '%.4f' % p for p in performance]))
print('net change of top2_stay30_normal_cost_50: %.4f'%(top2_stay30_normal_cost_50/top2_stay30_normal_cost_20))
print('net change of top2_coef_based_normal_cost_50: %.4f'%(top2_coef_based_normal_cost_50/top2_coef_based_normal_cost_20))
print('net change of top5_stay30_no_cost_50: %.4f'%(top5_stay30_no_cost_50/top5_stay30_no_cost_20))
print('net change of top5_stay30_normal_cost_50: %.4f'%(top5_stay30_normal_cost_50/top5_stay30_normal_cost_20))
print('net change of top5_coef_based_normal_cost_50: %.4f'%(top5_coef_based_normal_cost_50/top5_coef_based_normal_cost_20))

# ----------------------------------------------------------------------------------------

tpd_1_50 = int(days_count_50.split(',')[0].split(':')[1])
npd_1_50 = int(days_count_50.split(',')[1].split(':')[1])
tpd_3_50 = int(days_count_50.split(',')[2].split(':')[1])
npd_3_50 = int(days_count_50.split(',')[3].split(':')[1])
tpd_10_50 = int(days_count_50.split(',')[4].split(':')[1])
npd_10_50 = int(days_count_50.split(',')[5].split(':')[1])

tpd_1_63 = int(days_count_63.split(',')[0].split(':')[1])
npd_1_63 = int(days_count_63.split(',')[1].split(':')[1])
tpd_3_63 = int(days_count_63.split(',')[2].split(':')[1])
npd_3_63 = int(days_count_63.split(',')[3].split(':')[1])
tpd_10_63 = int(days_count_63.split(',')[4].split(':')[1])
npd_10_63 = int(days_count_63.split(',')[5].split(':')[1])

tn_1_ratio = (tpd_1_63 - tpd_1_50) / ( npd_1_63 - npd_1_50 )
tn_3_ratio = (tpd_3_63 - tpd_3_50) / ( npd_3_63 - npd_3_50 )
tn_10_ratio = (tpd_10_63 - tpd_10_50) / ( npd_10_63 - npd_10_50 )

performance_step50_list = [ float(segment.split(':')[1]) for segment in performance_step50_str.split(',') ]
performance_step63_list = [ float(segment.split(':')[1]) for segment in performance_step63_str.split(',') ]

top5_stay30_no_cost_63 = float(net_asset_63.split(',')[0].split(':')[1])
top5_stay30_normal_cost_63 = float(net_asset_63.split(',')[1].split(':')[1])
top2_stay30_normal_cost_63 = float(net_asset_63.split(',')[2].split(':')[1])
top5_coef_based_normal_cost_63 = float(net_asset_63.split(',')[3].split(':')[1])
top2_coef_based_normal_cost_63 = float(net_asset_63.split(',')[4].split(':')[1])

A = 50
B = 13

performance = []
for i in range(0, 3):
    score = (performance_step63_list[i] * (A+B) - performance_step50_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus, 50 - 63')
print('%.4f,'%tn_1_ratio, '%.4f,'%tn_3_ratio, '%.4f,'%tn_10_ratio)
#print('%.4f'%sum(performance))
print(', '.join([ '%.4f' % p for p in performance]))
print('net change of top2_stay30_normal_cost_63: %.4f'%(top2_stay30_normal_cost_63/top2_stay30_normal_cost_50))
print('net change of top2_coef_based_normal_cost_63: %.4f'%(top2_coef_based_normal_cost_63/top2_coef_based_normal_cost_50))
print('net change of top5_stay30_no_cost_63: %.4f'%(top5_stay30_no_cost_63/top5_stay30_no_cost_50))
print('net change of top5_stay30_normal_cost_63: %.4f'%(top5_stay30_normal_cost_63/top5_stay30_normal_cost_50))
print('net change of top5_coef_based_normal_cost_63: %.4f'%(top5_coef_based_normal_cost_63/top5_coef_based_normal_cost_50))
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
