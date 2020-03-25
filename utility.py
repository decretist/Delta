#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 24 March 2020
# 10 March 2020
import math
import matplotlib.pyplot as pp
import re
import statistics

def write_csv(dict_of_dicts, filename):
    '''
    23-24 March 2020
    Write out the contents of a dictionary of dictionaries as a CSV file.
    The multidimensional dictionary is currently in column-major order,
    which is probably wrong.
    '''
    f = open(filename, 'w')
    cols = list(dict_of_dicts.keys())
    rows = list(dict_of_dicts[cols[0]].keys())
    f.write(',' + ','.join(cols) + '\n') # column headers
    for row in rows:
        f.write(row)
        for col in cols:
            f.write(',' + str(dict_of_dicts[col][row]))
        f.write('\n')
    f.close()

def regression_slope(data_points):
    n = len(data_points)
    x_values, y_values = zip(*data_points)
    x_bar = statistics.mean(x_values)
    y_bar = statistics.mean(y_values)
    xy_sum = 0
    x_squared_sum = 0
    for i in range(n):
        xy_sum += x_values[i] * y_values[i]
        x_squared_sum += x_values[i] ** 2
    return (xy_sum - n * x_bar * y_bar) / (x_squared_sum - n * x_bar ** 2)

def plot_regression(data_points):
    x_values, y_values = zip(*data_points)
    x_bar = statistics.mean(x_values)
    y_bar = statistics.mean(y_values)
    slope = regression_slope(data_points)
    x_values = [0, max(x_values)]
    y_values = []
    for x in x_values:
        y_values.append(y_bar + slope * (x - x_bar))
    pp.plot(x_values, y_values)
    return slope

def plot_data_bar(data_points):
    x_values, y_values = zip(*data_points)
    pp.bar(x_values, y_values)
    pp.ylabel('frequency')

def plot_data_scatter(data_points):
    x_values, y_values = zip(*data_points)
    pp.scatter(x_values, y_values)
    pp.xlabel('$log_{e}$ rank')
    pp.ylabel('$log_{e}$ frequency')

def logify(data_points):
    x_tmp, y_tmp = zip(*data_points)
    x_values = list(x_tmp)
    y_values = list(y_tmp)
    x_log = [math.log(x) for x in x_values]
    y_log = [math.log(y) for y in y_values]
    return list(zip(x_log, y_log))

def frequencies(tokens):
    '''create and return token frequency dictionary'''
    types = list(set(tokens))
    tmp = dict.fromkeys(types, 0)
    for token in tokens: tmp[token] += 1
    token_frequencies = {
        key: value for key, value in sorted(tmp.items(),
        key = lambda item: (-item[1], item[0]))
    }
    return token_frequencies

def rank_frequencies(token_frequencies):
    '''create and return dictionary with token as key
    and rank-frequency pair as value'''
    tokens = list(token_frequencies.keys())
    frequencies = list(token_frequencies.values())
    pairs = []
    for rank in range(0, len(frequencies)):
        pairs.append((rank + 1, frequencies[rank]))
    token_rank_frequencies = dict(zip(tokens, pairs))
    return token_rank_frequencies
    
def tokenize(filename):
    '''open text file and return list of tokens'''
    text = open(filename, 'r').read().lower()
    tokens = [word for word in re.split('\W', text) if word != '']
    return tokens

def type_token_ratio(tokens):
    '''calculate and return type-token ratio for list of tokens'''
    types = list(set(tokens))
    type_token_ratio = len(types) / len(tokens)
    return type_token_ratio

def zipf_distrib(n, scale, **kwargs):
    '''
    11 March 2020
    generates and returns a scaled list of Zipf distribution rank-frequency
    pairs of length n, e.g., zipf_distrib(4, 1000) returns:
    [(1, 1000), (2, 500), (3, 333), (4, 250)]
    '''
    x_values = [x for x in range(1, n + 1)]
    if 'slope' in kwargs:
        slope = kwargs['slope']
        y_values = [round((1 / pow(x, -slope)) * scale) for x in x_values]
    else:
        y_values = [round((1 / x) * scale) for x in x_values]
    rank_frequency_pairs = list(zip(x_values, y_values))
    return rank_frequency_pairs

