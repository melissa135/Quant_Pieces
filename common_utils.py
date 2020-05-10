import math


def equal_mapping(num):
    return num

def log_change_single(num):
    num_log = 100 * math.log(1.0 + num/100.0)
    return num_log

def log_change_single_reverse(num_log):
    num = 100 * (math.exp(num_log/100.0) - 1)
    return num

def reach_limit(input_5min):
    flag = 0 # 0 for normal, 1 for limit_up, -1 for limit_down
    changes_5min = input_5min.tolist()
    anchor = conf['INTERCEPT_5MIN']
    # the rule is supposed the price is larger than 3.0
    if (abs(changes_5min[anchor]-changes_5min[anchor+1]) < 0.001) and \
            (abs(changes_5min[anchor+1]-changes_5min[anchor+2]) < 0.001) :
        if (changes_5min[anchor] > 9.9):
            flag = 1
        if (changes_5min[anchor] < -9.9):
            flag = -1
    return flag
