#!/usr/local/bin/python3
#
# Paul Evans (10evans@cua.edu)
# 21-22 February 2020
#
import matplotlib.pyplot as pp
import re
import zipf

def plot_log_pairs(pairs, stop):
    zipf.plot_data_scatter(zipf.logify(pairs[0:stop]))
    slope = zipf.plot_regression(zipf.logify(pairs[0:stop]))
    pp.title(
        f"actual distribution for {stop} MFWs from Gratian's " +
        '$\it{Decretum}$' +
        f'\n(log-log, slope = {slope:.4f})'
    )
    pp.show()

def main():
    text = open('./detagged.txt', 'r').read().lower()
    tokens = [word for word in re.split('\W', text) if word != '']
    types = list(set(tokens))
    type_token_ratio = len(types) / len(tokens)
    print(f'Type-token ratio: {type_token_ratio:.4f}')
    tmp = dict.fromkeys(types, 0)
    # for type in types: tmp[type] = tokens.count(type)
    # using list.count() method results in bad performance:
    # 4m42.915s versus 0m0.465s
    for token in tokens: tmp[token] += 1
    token_frequencies = {
        key: value for key, value in sorted(tmp.items(),
        key = lambda item: (-item[1], item[0]))
    }
    #
    # rank-frequency data for Gratian's Decretum
    #
    words = list(token_frequencies.keys())
    frequencies = list(token_frequencies.values())
    #
    print(sum(frequencies[:402]))
    print(len(tokens) // 2)
    print(sum(frequencies[:403]))
    #
    pairs = []
    for i in range(0, len(frequencies)): pairs.append((i + 1, frequencies[i]))
    word_pair_dict = dict(zip(words, pairs))
    #
    for stop in [10, 20, 40, 400, 4000, 40000, len(pairs)]:
        plot_log_pairs(pairs, stop)

if __name__ == '__main__':
    main()
