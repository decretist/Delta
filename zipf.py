#!/usr/local/bin/python3
#
# Paul Evans (10evans@cua.edu)
# 13-20 February 2020
#
import math
import matplotlib.pyplot as pp
import statistics

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
    pp.xticks([5, 10, 15, 20])
    pp.xlabel('rank')
    pp.ylabel('word count')

def plot_data_bar_20(word_pair_dict):
    words = list(word_pair_dict.keys())
    xy_values = list(word_pair_dict.values())
    x_values, y_values = zip(*xy_values)
    pp.bar(x_values, y_values)
    pp.xticks(x_values, words, rotation='vertical')
    pp.ylabel('word count')

def plot_data_bar_400(word_pair_dict):
    words = list(word_pair_dict.keys())
    xy_values = list(word_pair_dict.values())
    x_values, y_values = zip(*xy_values)
    pp.bar(x_values, y_values)
    pp.xticks([100, 200, 300, 400])
    pp.ylabel('word count')

def plot_data_bar_all(word_pair_dict):
    words = list(word_pair_dict.keys())
    xy_values = list(word_pair_dict.values())
    x_values, y_values = zip(*xy_values)
    pp.bar(x_values, y_values)
    pp.xticks([10000, 20000, 30000, 40000])
    pp.ylabel('word count')

def plot_data_scatter(data_points):
    x_values, y_values = zip(*data_points)
    pp.scatter(x_values, y_values)
    pp.xlabel('$log_{e}$ rank')
    pp.ylabel('$log_{e}$ word count')

def logify(data_points):
    x_tmp, y_tmp = zip(*data_points)
    x_values = list(x_tmp)
    y_values = list(y_tmp)
    x_log = [math.log(x) for x in x_values]
    y_log = [math.log(y) for y in y_values]
    return list(zip(x_log, y_log))

def main():
    #
    # rank-frequency data for Gratian's Decretum
    #
    word_pair_dict = eval(open('./dictionary.txt', 'r').read())
    words = list(word_pair_dict.keys())
    pairs = list(word_pair_dict.values())
    #
    # actual distribution for 20 MFWs from Gratian's Decretum
    # (bar plot)
    #
    plot_data_bar_20(dict(zip(words[0:20], pairs[0:20])))
    pp.title("actual distribution for 20 MFWs from Gratian's $\it{Decretum}$")
    pp.show()
    #
    # actual distribution for 20 MFWs from Gratian's Decretum
    # (log-log scatter plot)
    #
    plot_data_scatter(logify(pairs[0:20]))
    slope = plot_regression(logify(pairs[0:20]))
    pp.title("actual distribution for 20 MFWs from Gratian's $\it{Decretum}$\n(log-log, slope = " + f'{slope:.4f})')
    pp.show()
    #
    # actual distribution for 400 MFWs from Gratian's Decretum
    # (bar plot)
    #
    plot_data_bar_400(dict(zip(words[0:400], pairs[0:400])))
    pp.title("actual distribution for 400 MFWs from Gratian's $\it{Decretum}$")
    pp.show()
    #
    # actual distribution for 400 MFWs from Gratian's Decretum
    # (log-log scatter plot)
    #
    plot_data_scatter(logify(pairs[0:400]))
    slope = plot_regression(logify(pairs[0:400]))
    pp.title("actual distribution for 400 MFWs from Gratian's $\it{Decretum}$\n(log-log, slope = " + f'{slope:.4f})')
    pp.show()
    #
    # actual distribution for all words in Gratian's Decretum
    # (bar plot)
    #
    plot_data_bar_all(dict(zip(words, pairs)))
    pp.title("actual distribution for all words in Gratian's $\it{Decretum}$")
    pp.show()
    #
    # actual distribution for all words in Gratian's $\it{Decretum}$
    # (log-log scatter plot)
    #
    plot_data_scatter(logify(pairs))
    slope = plot_regression(logify(pairs))
    pp.title("actual distribution for all words in Gratian's $\it{Decretum}$\n(log-log, slope = " + f'{slope:.4f})')
    pp.show()

if __name__ == "__main__":
    main()

