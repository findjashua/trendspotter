import os
from datetime import datetime, timedelta
import traceback, json, csv

def get_src_dir():
    return '/Users/jashua/Dropbox/stocks/prices'

def get_filenames():
    return os.listdir(get_src_dir())

def get_date(datestring):
    [year, month, day] = datestring.split('-')
    return datetime(int(year), int(month), int(day))

def get_ohlc(bars):
    d = [bar[0] for bar in bars]
    o = [float(bar[1]) for bar in bars]
    h = [float(bar[2]) for bar in bars]
    l = [float(bar[3]) for bar in bars]
    c = [float(bar[4]) for bar in bars]
    v = [float(bar[5]) for bar in bars]
    return [d, o, h, l, c, v]

def get_bar_series(filename, num_periods, offset=0):
    src_dir = get_src_dir()
    path = '{}/{}'.format(src_dir, filename)
    csv_reader = csv.reader(open(path, 'rb'))
    rows = [row for row in csv_reader]
    rows.reverse()
    return get_ohlc(rows)

def truncate(val):
    return float('{:.4f}'.format(val))

def pretty_print(picks):
    for pick in picks:
        print json.dumps(pick, indent=4)
        print '==============================================================='
    print len(picks)

def get_ma(prices, interval, num_days):
    return [sum(prices[i:i+interval])/interval for i in range(interval+num_days)]

def recent_high(bars, window_l, window_s):
    return max([float(bar[2]) for bar in bars[:window_s]]) == max([float(bar[2]) for bar in bars[:window_l]])

def recent_low(bars, window_l, window_s):
    return min([float(bar[3]) for bar in bars[:window_s]]) == min([float(bar[3]) for bar in bars[:window_l]])

def get_min_ratio(o, h, l, c, left, right):
    if right-left < 0:
        return float('inf')

    if right-left is 0:
        return l[right]/h[left]

    if right-left is 1:
        left_ratio = get_min_ratio(o, h, l, c, left, left)
        right_ratio = get_min_ratio(o, h, l, c, right, right)
        crossover_ratio = l[right]/h[left]
        return min(left_ratio, right_ratio, crossover_ratio)

    opens = o[left:right+1]
    highs = h[left:right+1]
    lows = l[left:right+1]
    closes = c[left:right+1]
    high = max(highs)
    high_index = left+highs.index(high)
    low = min(lows)
    low_index = left+lows.index(low)

    if high_index <= low_index:
        return low/high

    if low_index - left > 1:
        high_left = max(h[left:low_index])
        left_ratio = low/high_left
    else:
        left_ratio = get_min_ratio(o, h, l, c, left, left)

    if right - high_index > 1:
        low_right = min(l[high_index+1:right+1])
        right_ratio = low_right/high
    else:
        right_ratio = get_min_ratio(o, h, l, c, right, right)

    mid_ratio = get_min_ratio(o, h, l, c, low_index+1, high_index-1)

    return min(left_ratio, right_ratio, mid_ratio)

def get_max_drop(ohlc_series, window):
    try:
        [o, h, l, c] = [series[:window] for series in ohlc_series]
        [series.reverse() for series in [o, h, l, c]]
        ratio = get_min_ratio(o, h, l, c, 0, window-1)
        return truncate(100*(1-ratio))
    except:
        traceback.print_exc()

def get_max_ratio(o, h, l, c, left, right):
    if right-left < 0:
        return -1*float('inf')

    if right-left is 0:
        return h[right]/l[left]

    if right-left is 1:
        left_ratio = get_max_ratio(o, h, l, c, left, left)
        right_ratio = get_max_ratio(o, h, l, c, right, right)
        crossover_ratio = h[right]/l[left]
        return max(left_ratio, right_ratio, crossover_ratio)

    opens = o[left:right+1]
    highs = h[left:right+1]
    lows = l[left:right+1]
    closes = c[left:right+1]
    high = max(highs)
    high_index = left+highs.index(high)
    low = min(lows)
    low_index = left+lows.index(low)

    if high_index <= low_index:
        return high/low

    if low_index > left:
        low_left = min(l[left:low_index])
        left_ratio = high/low_left
    else:
        left_ratio = get_max_ratio(o, h, l, c, left, left)

    if high_index < right:
        high_right = max(l[high_index+1:right+1])
        right_ratio = high_right/low
    else:
        right_ratio = get_max_ratio(o, h, l, c, right, right)

    mid_ratio = get_max_ratio(o, h, l, c, low_index+1, high_index-1)

    return max(left_ratio, right_ratio, mid_ratio)

def get_max_jump(bars, window):
    try:
        [o, h, l, c] = [series[:window].reverse() for series in ohlc_series]
        ratio = get_max_ratio(o, h, l, c, 0, window-1)
        return truncate(100*(ratio-1))
    except:
        traceback.print_exc()
