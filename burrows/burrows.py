#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 11-14 March 2020
import itertools
import math
import statistics
import sys
sys.path.append('..')
import utility as u
def main():
    '''
    Assemble a large corpus made up of texts written by an arbitrary
    number of authors; let’s say that number of authors is x.
    '''
    test = 'cases' # only have to change this one line
    authors = ['cases', 'laws', 'marriage', 'other', 'penance', 'second']
    authors.remove(test)
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
    corp_f_dict = {}
    empty = dict.fromkeys(mfws, 0)
    for author in authors:
        corp_f_dict[author] = empty.copy()
        subcorpus = u.tokenize('./corpus/' + author + '.txt')
        subcorpus_frequencies = u.frequencies(subcorpus)
        for word in mfws:
            corp_f_dict[author][word] = (subcorpus_frequencies.get(word, 0) / len(subcorpus)) * 1000
        u.write_csv(corp_f_dict, './subcorpus_frequencies.csv')
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
        corp_f_list = []
        for author in authors:
            corp_f_list.append(corp_f_dict[author][word])
        means[word] = statistics.mean(corp_f_list)
        stdevs[word] = statistics.stdev(corp_f_list)
    '''
    For each of the n features and x subcorpora, calculate a z-score
    describing how far away from the corpus norm the usage of this
    particular feature in this particular subcorpus happens to be.
    To do this, subtract the "mean of means" for the feature from
    the feature’s frequency in the subcorpus and divide the result
    by the feature’s standard deviation.
    '''
    corp_z_dict = {}
    for author in authors:
        corp_z_dict[author] = empty.copy()
        for word in mfws:
            corp_z_dict[author][word] = (corp_f_dict[author][word] - means[word]) / stdevs[word]
    '''
    Then, calculate the same z-scores for each feature in the text
    for which we want to determine authorship.
    '''
    test_tokens = []
    test_tokens = u.tokenize('./corpus/' + test + '.txt')
    test_frequencies = u.frequencies(test_tokens)
    test_f_dict = test_z_dict = empty.copy()
    for word in mfws:
       test_f_dict[word] = (test_frequencies.get(word, 0) / len(test_tokens)) * 1000
       # can collapse this into one loop
       test_z_dict[word] = (test_f_dict[word] - means[word]) / stdevs[word]
    print(test_z_dict)
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
    for author in authors:
        sum = 0
        for word in mfws:
            sum += math.fabs(corp_z_dict[author][word] - test_z_dict[word])
        delta = sum / len(mfws)
        print(test + "-" + author + " delta: " + str(delta))

if __name__ == '__main__':
    main()
