import util, traceback, math


def get_stats(filename, offset, period, window, min_delta, min_pctg, max_drawdown, history, min_volume):
    try:
        num_days = history['num_days']
        [d, o, h, l, c, v] = util.get_bar_series(filename, history['num_days'], offset)
        #print d[0], c[0], d[window['num_days']-1], c[window['num_days']-1]

        curr_to_high_ratio = h[0]/max(h)

        overall_drawdown = util.get_max_drop([o, h, l, c], num_days)

        deltas = [100*(c[i]/c[i+period] - 1) for i in range(window)]
        pctg = util.truncate(100*len([delta for delta in deltas if delta > min_delta])/len(deltas))
        min_delta = util.truncate(min(deltas))
        drawdown = util.get_max_drop([o, h, l, c], window)

        error = None

        if curr_to_high_ratio < history['curr_to_high_ratio']:
            error = 'curr to high ratio is {}'.format(curr_to_high_ratio)

        if overall_drawdown > history['max_drawdown']:
            error = 'overall_drawdown is {}'.format(overall_drawdown)

        if drawdown > max_drawdown:
            error = 'drawdown is {}'.format(max_drawdown)

        if pctg < min_pctg:
            error = 'pctg is {}'.format(pctg)

        if v[0] < min_volume:
            error = 'volume is {}'.format(v[0])

        stats = {
            'symbol': filename.split('.csv')[0],
            'min_delta': min_delta,
            'pctg': pctg,
            'drawdown': drawdown,
            'volume': v[0]
        }

        if error:
            #print error
            return None
        else:
            print stats
            return stats
    except:
        #traceback.print_exc()
        pass

filenames = util.get_filenames()
#filenames = ['kr.csv']

offset = 0 #for going back in time

period = 65
window = 130
min_delta = 1
min_pctg = 100
max_drawdown = 10

history = {
    'num_days': 500, # >= num_days + period,
    'curr_to_high_ratio': .8,
    'max_drawdown': 25
}

min_volume = 100000

stats_arr = [get_stats(filename, offset, period, window, min_delta, min_pctg, max_drawdown, history, min_volume) for filename in filenames]
stats_arr = [stats for stats in stats_arr if stats]

util.pretty_print(stats_arr)
print [stats['symbol'] for stats in stats_arr]
