days_count_20 = 'top1_tp_days: 520, top1_np_days: 480, top3_tp_days: 1536, top3_np_days: 1464, top10_tp_days: 5018, top10_np_days: 4980'
days_count_50 = 'top1_tp_days: 1285, top1_np_days: 1246, top3_tp_days: 3814, top3_np_days: 3787, top10_tp_days: 12228, top10_np_days: 13018'
days_count_65 = 'top1_tp_days: 1682, top1_np_days: 1607, top3_tp_days: 5014, top3_np_days: 4858, top10_tp_days: 16026, top10_np_days: 16764'

performance_step20_str = 'top1_log_avg: 0.3720, top3_log_avg: 0.3255, top10_log_avg: 0.2563'
performance_step50_str = 'top1_log_avg: 0.3294, top3_log_avg: 0.2412, top10_log_avg: 0.1384'
performance_step65_str = 'top1_log_avg: 0.3132, top3_log_avg: 0.2454, top10_log_avg: 0.1451'

net_asset_20 = 'top5_stay30_no_cost: 444.0749, top5_stay30_normal_cost: 82.2051, top2_stay30_normal_cost: 96.3548, top5_coef_based_normal_cost: 104.9066, top2_coef_based_normal_cost: 128.2328'
net_asset_50 = 'top5_stay30_no_cost: 511.4206, top5_stay30_normal_cost: 126.5357, top2_stay30_normal_cost: 374.2397, top5_coef_based_normal_cost: 146.0481, top2_coef_based_normal_cost: 380.3155'
net_asset_65 = 'top5_stay30_no_cost: 2582.7730, top5_stay30_normal_cost: 424.0524, top2_stay30_normal_cost: 1599.9776, top5_coef_based_normal_cost: 467.5546, top2_coef_based_normal_cost: 1239.4565'

tpd_1_20 = int(days_count_20.split(',')[0].split(':')[1])
npd_1_20 = int(days_count_20.split(',')[1].split(':')[1])
tpd_3_20 = int(days_count_20.split(',')[2].split(':')[1])
npd_3_20 = int(days_count_20.split(',')[3].split(':')[1])
tpd_10_20 = int(days_count_20.split(',')[4].split(':')[1])
npd_10_20 = int(days_count_20.split(',')[5].split(':')[1])

tpd_1_65 = int(days_count_65.split(',')[0].split(':')[1])
npd_1_65 = int(days_count_65.split(',')[1].split(':')[1])
tpd_3_65 = int(days_count_65.split(',')[2].split(':')[1])
npd_3_65 = int(days_count_65.split(',')[3].split(':')[1])
tpd_10_65 = int(days_count_65.split(',')[4].split(':')[1])
npd_10_65 = int(days_count_65.split(',')[5].split(':')[1])

tn_1_ratio = (tpd_1_65 - tpd_1_20) / ( npd_1_65 - npd_1_20 )
tn_3_ratio = (tpd_3_65 - tpd_3_20) / ( npd_3_65 - npd_3_20 )
tn_10_ratio = (tpd_10_65 - tpd_10_20) / ( npd_10_65 - npd_10_20 )

performance_step20_list = [ float(segment.split(':')[1]) for segment in performance_step20_str.split(',') ]
performance_step65_list = [ float(segment.split(':')[1]) for segment in performance_step65_str.split(',') ]

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
B = 45

performance = []
for i in range(0, 3):
    score = (performance_step65_list[i] * (A+B) - performance_step20_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus, 20 - 65')
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

tpd_1_65 = int(days_count_65.split(',')[0].split(':')[1])
npd_1_65 = int(days_count_65.split(',')[1].split(':')[1])
tpd_3_65 = int(days_count_65.split(',')[2].split(':')[1])
npd_3_65 = int(days_count_65.split(',')[3].split(':')[1])
tpd_10_65 = int(days_count_65.split(',')[4].split(':')[1])
npd_10_65 = int(days_count_65.split(',')[5].split(':')[1])

tn_1_ratio = (tpd_1_65 - tpd_1_50) / ( npd_1_65 - npd_1_50 )
tn_3_ratio = (tpd_3_65 - tpd_3_50) / ( npd_3_65 - npd_3_50 )
tn_10_ratio = (tpd_10_65 - tpd_10_50) / ( npd_10_65 - npd_10_50 )

performance_step50_list = [ float(segment.split(':')[1]) for segment in performance_step50_str.split(',') ]
performance_step65_list = [ float(segment.split(':')[1]) for segment in performance_step65_str.split(',') ]

top5_stay30_no_cost_65 = float(net_asset_65.split(',')[0].split(':')[1])
top5_stay30_normal_cost_65 = float(net_asset_65.split(',')[1].split(':')[1])
top2_stay30_normal_cost_65 = float(net_asset_65.split(',')[2].split(':')[1])
top5_coef_based_normal_cost_65 = float(net_asset_65.split(',')[3].split(':')[1])
top2_coef_based_normal_cost_65 = float(net_asset_65.split(',')[4].split(':')[1])

A = 50
B = 15

performance = []
for i in range(0, 3):
    score = (performance_step65_list[i] * (A+B) - performance_step50_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus, 50 - 65')
print('%.4f,'%tn_1_ratio, '%.4f,'%tn_3_ratio, '%.4f,'%tn_10_ratio)
#print('%.4f'%sum(performance))
print(', '.join([ '%.4f' % p for p in performance]))
print('net change of top2_stay30_normal_cost_65: %.4f'%(top2_stay30_normal_cost_65/top2_stay30_normal_cost_50))
print('net change of top2_coef_based_normal_cost_65: %.4f'%(top2_coef_based_normal_cost_65/top2_coef_based_normal_cost_50))
print('net change of top5_stay30_no_cost_65: %.4f'%(top5_stay30_no_cost_65/top5_stay30_no_cost_50))
print('net change of top5_stay30_normal_cost_65: %.4f'%(top5_stay30_normal_cost_65/top5_stay30_normal_cost_50))
print('net change of top5_coef_based_normal_cost_65: %.4f'%(top5_coef_based_normal_cost_65/top5_coef_based_normal_cost_50))
