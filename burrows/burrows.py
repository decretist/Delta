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
    corpus_frequencies = u.frequencies(corpus)
    corpus_most_frequent_words = (list(corpus_frequencies.keys()))[:30]
    '''
    For each of these n features, calculate the share of each of
    the x authors’ subcorpora represented by this feature, as a
    percentage of the total number of words.
    '''
    frequency_dictionary = {}
    empty = dict.fromkeys(list(corpus_frequencies.keys())[:30], 0)
    frequency_dictionary['mean'] = empty.copy()
    frequency_dictionary['stdev'] = empty.copy()
    for author in authors:
        frequency_dictionary[author] = empty.copy()
        subcorpus = u.tokenize('./corpus/' + author + '.txt')
        subcorpus_length = len(subcorpus)
        subcorpus_frequencies = u.frequencies(subcorpus)
        for word in corpus_most_frequent_words:
            frequency_dictionary[author][word] = (subcorpus_frequencies.get(word, 0) / subcorpus_length) * 1000
    '''
    Then, calculate the mean and the standard deviation of these x
    values and use them as the offical mean and standard deviation
    for this feature over the whole corpus. In other words, we will
    be using a mean of means instead of calculating a single value
    representing the share of the entire corpus represented by each
    word.
    '''
    for word in corpus_most_frequent_words:
        frequencies_list = []
        for author in authors:
            frequencies_list.append(frequency_dictionary[author][word])
        frequency_dictionary['mean'][word] = statistics.mean(frequencies_list)
        frequency_dictionary['stdev'][word] = statistics.stdev(frequencies_list)
    print(frequency_dictionary)

if __name__ == '__main__':
    main()
