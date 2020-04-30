days_count_50 = 'tp_days: 6334, np_days: 6166'
days_count_62 = 'tp_days: 7822, np_days: 7618'

tpd_50 = int(days_count_50.split(',')[0].split(':')[1])
npd_50 = int(days_count_50.split(',')[1].split(':')[1])

tpd_62 = int(days_count_62.split(',')[0].split(':')[1])
npd_62 = int(days_count_62.split(',')[1].split(':')[1])

p_count = tpd_62 - tpd_50 - ( npd_62 - npd_50 )

performance_step50_str = 'top1_avg: 0.3881, top2_avg: 0.2729, top3_avg: 0.2574, top4_avg: 0.2908, top5_avg: 0.2272'
performance_step50_list = [ float(segment.split(':')[1]) for segment in performance_step50_str.split(',') ]

performance_step62_str = 'top1_avg: 0.3514, top2_avg: 0.2586, top3_avg: 0.2432, top4_avg: 0.2731, top5_avg: 0.2352'
performance_step62_list = [ float(segment.split(':')[1]) for segment in performance_step62_str.split(',') ]

A = 50
B = 12

performance = []
for i in range(0, 5):
    score = (performance_step62_list[i] * (A+B) - performance_step50_list[i] * A)/B
    performance.append(score)

print('normal, random test A plus')
print(p_count)
print('%.4f'%sum(performance))
print(', '.join([ '%.4f' % p for p in performance]))

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
