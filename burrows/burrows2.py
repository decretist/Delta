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

def debug(foo, bar):
    print(foo, bar)

def main(): # driver
    samples = ['cases', 'laws', 'marriage', 'other', 'penance', 'second']
    for sample in samples:
        sample_list = samples[:] # sample_list = samples.copy()
        sample_list.remove(sample)
        # debug(sample, sample_list)
        # corpus = get_features(sample_list)
    # test first case only until working
    sample_list = samples.copy() # sample_list = samples[:]
    sample_list.remove('cases')
    mfws = get_features(sample_list, 30)
    print(mfws)

if __name__ == '__main__':
    main()

