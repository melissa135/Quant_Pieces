import math
from config_offline import conf


def equal_mapping(num):
    return num


def limit_log(num, lower=0.01, upper=100.0):
    if num < lower:
        num = lower
    elif num > upper:
        num = upper
    num_log = math.log(num)
    return num_log


def log_change_single(num):
    num_log = 100 * limit_log(1.0 + num/100.0)
    return num_log


def log_diff(numa, numb):
    diff = log_change_single(numa) - log_change_single(numb)
    return diff


def reletive_change_resize(num, resize):
    x = 1.0 + num/100.0
    x = x/resize
    x = 100.0*(x - 1.0)
    return x


def reach_limit(input_5min):
    flag = 0  # 0 for normal, 1 for limit_up, -1 for limit_down
    changes_5min = input_5min.tolist()
    anchor = conf['INTERCEPT_5MIN']
    # the rule is supposed the price is larger than 3.0
    if (abs(changes_5min[anchor]-changes_5min[anchor+1]) < 0.001) and \
            (abs(changes_5min[anchor+1]-changes_5min[anchor+2]) < 0.001) :
        if changes_5min[anchor] > 9.9:
            flag = 1
        if changes_5min[anchor] < -9.9:
            flag = -1
    return flag


def prepare_data_uniform_qfq(df_raw, begin_index, refer_index):
    # begin_index is the earliest day that need to calculate
    # do not include the dividend recorded in refer_index day
    sd_coef_current = 1.0
    cd_coef_current = 0.0
    sd_coef_list = [sd_coef_current for _ in range(0, len(df_raw))]
    cd_coef_list = [cd_coef_current for _ in range(0, len(df_raw))]
    df_raw['sd_coef'] = sd_coef_list
    df_raw['cd_coef'] = cd_coef_list

    for i in range(refer_index-1, begin_index-1, -1):
        c_d = df_raw.iloc[i]['cash_dividend']
        s_d = df_raw.iloc[i]['stock_dividend']
        sd_coef_current = sd_coef_current * (10 + s_d) / 10
        cd_coef_current = cd_coef_current * (10 + s_d) / 10 + c_d / 10
        df_raw.loc[i, 'sd_coef'] = sd_coef_current
        df_raw.loc[i, 'cd_coef'] = cd_coef_current

    return df_raw


def get_data_uniform_qfq(df_raw, column, index):

    result = df_raw.iloc[index][column]
    sd_coef = df_raw.iloc[index]['sd_coef']
    cd_coef = df_raw.iloc[index]['cd_coef']

    if (column == 'volume') or (column == 'vma5') or (column == 'vma20'):
        result = result * sd_coef
    else:
        result = (result - cd_coef) / sd_coef

    return result


def get_dividend(df_refer):
    #  for those tables which does not have cash/stock dividend column
    dividends = dict()

    for i in range(0, len(df_refer)):
        key = df_refer.iloc[i]['date']
        c_d = df_refer.iloc[i]['cash_dividend']
        s_d = df_refer.iloc[i]['stock_dividend']
        stock_dividend = 10.0 / (10.0 + s_d)
        cash_dividend = c_d / (10.0 + s_d)
        value = (cash_dividend, stock_dividend)
        dividends[key] = value

    return dividends


class Pred_Info(object):
    def __init__(self, stock, pred, target, actual, flag):
        self.stock = stock
        self.pred = pred
        self.target = target
        self.actual = actual
        self.flag = flag

    def __str__(self):
        string = '%s, %.4f, %.4f, %.4f, %d' % (self.stock, self.pred, self.target, self.actual, self.flag)
        return string