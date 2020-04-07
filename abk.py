#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
#  2 Apr 2020
# 18 Mar 2020
import matplotlib.pyplot as pp
import utility as u

def main():
    filenames = ['Gratian0.txt', 'Gratian1.txt', 'Gratian2.txt']
    tokens = []
    for filename in filenames:
        tokens += u.tokenize('./corpus/' + filename)
    frequencies = u.frequencies(tokens)
    stop = 31 # Figure_Zy
    # stop = len(frequencies) # Figure_Zz
    words = []
    occurences = []
    for b in range(1, stop): # Number of Occurences (b)
        a = 0 # Number of Words (a)
        for value in list(frequencies.values()):
            if value == b: a += 1
        k = a * b * b # ab^2 = k formulation of Zipf's law
        if a == 0: continue # log(0) throws ValueError: math domain error 
        words.append(a)
        occurences.append(b)
    u.plot_data_scatter(u.logify(zip(words, occurences)))
    slope = u.plot_regression(u.logify(zip(words, occurences)))
    pp.xlabel('Number of Words')
    pp.ylabel('Number of Occurences')
    pp.title('$ab^2 = k$\n(log-log, slope = ' + f'{slope:.4f})')
    pp.savefig('./PNGs/Figure_Zy')
    # pp.savefig('./PNGs/Figure_Zz')
    pp.show()

if __name__ == '__main__':
    main()
