#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 24-25 March 2020
import math
import statistics
import sys
sys.path.append('..')
import utility as u

path = './corpus/'

def get_features(texts, n):
    '''
    Assemble a large corpus made up of texts written by an arbitrary
    number of authors; let’s say that number of authors is x.
    '''
    corpus = []
    for text in texts:
        corpus += u.tokenize(path + text + '.txt')
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
    frequencies = {}
    empty = dict.fromkeys(features, 0)
    for subcorpus in subcorpora:
        frequencies[subcorpus] = empty.copy()
        subcorpus_tokens = u.tokenize(path + subcorpus + '.txt')
        subcorpus_frequencies = u.frequencies(subcorpus_tokens)
        for feature in features:
            frequencies[subcorpus][feature] = (subcorpus_frequencies.get(feature, 0) / len(subcorpus_tokens)) * 1000
    return frequencies

def get_means(frequencies):
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

def get_z_scores(subcorpora, frequencies):
    '''
    For each of the n features and x subcorpora, calculate a z-score
    describing how far away from the corpus norm the usage of this
    particular feature in this particular subcorpus happens to be.
    To do this, subtract the "mean of means" for the feature from
    the feature’s frequency in the subcorpus and divide the result
    by the feature’s standard deviation.
    '''
    z_scores = {}
    features = list(frequencies[subcorpora[0]].keys())
    for subcorpus in subcorpora:
        z_scores[subcorpus] = dict.fromkeys(features, 0)
        for feature in features:
            z_scores[subcorpus][feature] = (frequencies[subcorpus][feature] - frequencies['means'][feature]) / frequencies['stdevs'][feature]
    return z_scores

def add_test_values(test, features, frequencies, z_scores):
    '''
    Then, calculate the same z-scores for each feature in the text
    for which we want to determine authorship.
    '''
    test_tokens = []
    test_tokens = u.tokenize(path + test + '.txt')
    test_frequencies = u.frequencies(test_tokens)
    frequencies[test] = dict.fromkeys(features, 0)
    z_scores[test] = dict.fromkeys(features, 0)
    for feature in features:
       frequencies[test][feature] = (test_frequencies.get(feature, 0) / len(test_tokens)) * 1000
       z_scores[test][feature] = (frequencies[test][feature] - frequencies['means'][feature]) / frequencies['stdevs'][feature]
    return (frequencies, z_scores)

def get_deltas(subcorpora, features, z_scores, test):
    '''
    Finally, calculate a delta score comparing the anonymous paper
    with each candidate’s subcorpus. To do this, take the average
    of the absolute values of the differences between the z-scores
    for each feature between the anonymous paper and the candidate’s
    subcorpus. (Read that twice!) This gives equal weight to each
    feature, no matter how often the words occur in the texts;
    otherwise, the top 3 or 4 features would overwhelm everything
    else.
    '''
    print(',' + ','.join(subcorpora))
    print(test, end = '')
    for subcorpus in subcorpora:
        sum = 0
        for feature in features:
            sum += math.fabs(z_scores[subcorpus][feature] - z_scores[test][feature])
        delta = sum / len(features)
        print(',' + str(delta), end = '')
    print('\n')

def main(): # driver
    samples = ['cases', 'laws', 'marriage', 'other', 'penance', 'second']
    for sample in samples:
        sample_list = samples.copy() # sample_list = samples[:]
        sample_list.remove(sample)
        features = get_features(sample_list, 30)
        tmp = get_frequencies(features, sample_list)
        tmp1 = get_means(tmp)
        tmp2 = get_z_scores(sample_list, tmp)
        f, z = add_test_values(sample, features, tmp1, tmp2)
        get_deltas(sample_list, features, z, sample)

if __name__ == '__main__':
    main()

