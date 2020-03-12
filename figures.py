#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 10-11 March 2020
import itertools
import matplotlib.pyplot as pp
import utility as u

def figure_za(pairs):
    n = len(pairs)
    u.plot_data_bar(pairs)
    pp.title(f'theoretical Zipf distribution for {n} MFWs')
    pp.xticks([(x + 1) * 5 for x in range(n // 5)])
    pp.show()

def figure_zb(pairs):
    n = len(pairs)
    u.plot_data_scatter(u.logify(pairs[0:n]))
    slope = u.plot_regression(u.logify(pairs[0:n]))
    pp.title(f'theoretical Zipf distribution for {n} MFWs\n(log-log, slope = {slope:.2f})')
    pp.show()

def figure_zc(word_pair_dict):
    words = list(word_pair_dict.keys())
    xy_values = list(word_pair_dict.values())
    x_values, y_values = zip(*xy_values)
    pp.figure(figsize=[9.6, 6.4])
    pp.bar(x_values, y_values)
    pp.xticks(x_values, words, rotation='vertical')
    pp.ylabel('frequency')
    pp.title(f'actual Zipf distribution for {len(x_values)} MFWs')
    pp.show()

def figure_zd(pairs):
    n = len(pairs)
    u.plot_data_scatter(u.logify(pairs[0:n]))
    slope = u.plot_regression(u.logify(pairs[0:n]))
    pp.title(f'actual Zipf distribution for {n} MFWs\n(log-log, slope = {slope:.2f})')
    pp.show()

def main():
    filenames = ['Gratian0.txt', 'Gratian1.txt', 'Gratian2.txt']
    tokens = []
    for filename in filenames:
        tokens += u.tokenize('./corpus/' + filename)
    tmp = u.rank_frequencies(u.frequencies(tokens))
    actual = list(tmp.values())
    scale = actual[0][1]
    # 30 is a commonly used number in Burrows's articles
    theoretical = u.zipf_distrib(30, scale)
    figure_za(theoretical)
    figure_zb(theoretical)
    figure_zc(dict(itertools.islice(tmp.items(), 30)))
    figure_zd(actual[0:30])
    figure_zd(actual)

if __name__ == '__main__':
    main()

