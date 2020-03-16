#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 11-14 March 2020
import itertools
import statistics
import utility as u
def main():
    '''
    Assemble a large corpus made up of texts written by an arbitrary
    number of authors; let’s say that number of authors is x.
    '''
    authors = ['cases', 'laws', 'marriage', 'other', 'penance', 'second']
    corpus = []
    for author in authors:
        corpus += u.tokenize('./corpus/' + author + '.txt')
    '''
    Find the n most frequent words in the corpus to use as features.
    '''
    mfws = list(u.frequencies(corpus).keys())[:30]
    '''
    For each of these n features, calculate the share of each of
    the x authors’ subcorpora represented by this feature, as a
    percentage of the total number of words.
    '''
    f_dict = {}
    empty = dict.fromkeys(mfws, 0)
    for author in authors:
        f_dict[author] = empty.copy()
        subcorpus = u.tokenize('./corpus/' + author + '.txt')
        subcorpus_frequencies = u.frequencies(subcorpus)
        for word in mfws:
            f_dict[author][word] = (subcorpus_frequencies.get(word, 0) / len(subcorpus)) * 1000
    '''
    Then, calculate the mean and the standard deviation of these x
    values and use them as the offical mean and standard deviation
    for this feature over the whole corpus. In other words, we will
    be using a mean of means instead of calculating a single value
    representing the share of the entire corpus represented by each
    word.
    '''
    means = empty.copy()
    stdevs = empty.copy()
    for word in mfws:
        f_list = []
        for author in authors:
            f_list.append(f_dict[author][word])
        means[word] = statistics.mean(f_list)
        stdevs[word] = statistics.stdev(f_list)
    '''
    For each of the n features and x subcorpora, calculate a z-score
    describing how far away from the corpus norm the usage of this
    particular feature in this particular subcorpus happens to be.
    To do this, subtract the "mean of means" for the feature from
    the feature’s frequency in the subcorpus and divide the result
    by the feature’s standard deviation.
    '''
    z_dict = {}
    for author in authors:
        z_dict[author] = empty.copy()
        for word in mfws:
            z_dict[author][word] = (f_dict[author][word] - means[word]) / stdevs[word]
    print(z_dict)

if __name__ == '__main__':
    main()
