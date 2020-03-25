#!/usr/local/bin/python3
# Paul Evans (10evans@cua.edu)
# 24 March 2020
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

def get_subcorp_freqs(features, subcorpora):
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
    tmp = get_subcorp_freqs(mfws, sample_list)
    u.write_csv(tmp, './subcorpora_frequencies.csv')

if __name__ == '__main__':
    main()

