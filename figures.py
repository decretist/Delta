#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 10-12 March 2020
import itertools
import matplotlib.pyplot as pp
import utility as u

def plot_data_bar(tmp):
    if isinstance(tmp, list):
        xy_values = tmp
        u.plot_data_bar(xy_values)
        pp.xlabel('rank')
    elif isinstance(tmp, dict):
        words = list(tmp.keys())
        xy_values = list(tmp.values())
        u.plot_data_bar(xy_values)
        x_values, y_values = zip(*xy_values)
        pp.xticks(x_values, words, rotation='vertical')

def figure_za(pairs):
    plot_data_bar(pairs)
    pp.title(f'theoretical Zipf distribution for {len(pairs)} MFWs')
    pp.xticks([(x + 1) * 5 for x in range(len(pairs) // 5)])
    pp.savefig('./PNGs/Figure_Za')
    pp.show()

def figure_zb(pairs):
    n = len(pairs)
    u.plot_data_scatter(u.logify(pairs[0:n]))
    slope = u.plot_regression(u.logify(pairs[0:n]))
    pp.title(f'theoretical Zipf distribution for {n} MFWs\n(log-log, slope = {slope:.1f})')
    pp.savefig('./PNGs/Figure_Zb')
    pp.show()

def figure_zc(word_pair_dict):
    pp.figure(figsize=[9.6, 6.4])
    plot_data_bar(word_pair_dict)
    pp.title(f"actual Zipf distribution for {len(word_pair_dict)} MFWs from Gratian's " + '$\it{dicta}$')
    pp.savefig('./PNGs/Figure_Zc')
    pp.show()

def figure_zd(pairs):
    n = len(pairs)
    u.plot_data_scatter(u.logify(pairs[0:n]))
    slope = u.plot_regression(u.logify(pairs[0:n]))
    pp.title(f"actual Zipf distribution for {n} MFWs from Gratian's " + '$\it{dicta}$\n' + f'(log-log, slope = {slope:.4f})')
    pp.savefig('./PNGs/Figure_Zd')
    pp.show()

def figure_ze(pairs):
    n = len(pairs)
    u.plot_data_scatter(u.logify(pairs[0:n]))
    slope = u.plot_regression(u.logify(pairs[0:n]))
    pp.title(f"actual Zipf distribution for {n} MFWs from Gratian's " + '$\it{dicta}$\n' + f'(log-log, slope = {slope:.4f})')
    pp.savefig('./PNGs/Figure_Ze')
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
    figure_ze(actual)

if __name__ == '__main__':
    main()

