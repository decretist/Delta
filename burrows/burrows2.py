#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 24 March 2020
import statistics
import sys
sys.path.append('..')
import utility as u

def get_features(texts, n):
    '''
    Assemble a large corpus made up of texts written by an arbitrary
    number of authors; let’s say that number of authors is x.
    '''
    corpus = []
    for text in texts:
        corpus += u.tokenize('./corpus/' + text + '.txt')
    '''
    Find the n most frequent words in the corpus to use as features.
    '''
    features = list(u.frequencies(corpus).keys())[:n]
    return features

def get_frequencies(features, subcorpora):
    '''
    For each of these n features, calculate the share of each of
    the x authors’ subcorpora represented by this feature, as a
    percentage of the total number of words.
    '''
    subcorpora_frequencies = {}
    empty = dict.fromkeys(features, 0)
    for subcorpus in subcorpora:
        subcorpora_frequencies[subcorpus] = empty.copy()
        subcorpus_tokens = u.tokenize('./corpus/' + subcorpus + '.txt')
        subcorpus_frequencies = u.frequencies(subcorpus_tokens)
        for feature in features:
            subcorpora_frequencies[subcorpus][feature] = (subcorpus_frequencies.get(feature, 0) / len(subcorpus_tokens)) * 1000
    return subcorpora_frequencies

def get_statistics(frequencies):
    '''
    Then, calculate the mean and the standard deviation of these x
    values and use them as the offical mean and standard deviation
    for this feature over the whole corpus. In other words, we will
    be using a mean of means instead of calculating a single value
    representing the share of the entire corpus represented by each
    word.
    '''
    subcorpora = list(frequencies.keys())
    features = list(frequencies[subcorpora[0]].keys())
    frequencies['means'] = dict.fromkeys(features, 0)
    frequencies['stdevs'] = dict.fromkeys(features, 0)
    for feature in features:
        frequency_list = []
        for subcorpus in subcorpora:
            frequency_list.append(frequencies[subcorpus][feature])
        frequencies['means'][feature] = statistics.mean(frequency_list)
        frequencies['stdevs'][feature] = statistics.stdev(frequency_list)
    return frequencies

def main(): # driver
    samples = ['cases', 'laws', 'marriage', 'other', 'penance', 'second']
    for sample in samples:
        sample_list = samples[:] # sample_list = samples.copy()
        sample_list.remove(sample)
        # corpus = get_features(sample_list)
    # test first case only until working
    sample_list = samples.copy() # sample_list = samples[:]
    sample_list.remove('cases')
    mfws = get_features(sample_list, 30)
    tmp = get_frequencies(mfws, sample_list)
    tmp = get_statistics(tmp)
    u.write_csv(tmp, './tmp.csv')

if __name__ == '__main__':
    main()

