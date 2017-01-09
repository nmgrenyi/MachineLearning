from __future__ import division
#'/' Return mathematical result of division. For truncating division, use '//' instead
from collections import Counter
import numpy as np



def entropy(Y):
    #Calculate the entropy for current dataset.
    distribution = Counter(Y)
    e = 0.0
    total = len(Y)
    for y, num_y in distribution.items():
        probability_y = (num_y / total)
        e += (probability_y) * np.log(probability_y)
    return -e


def information_gain(y, y_true, y_false):
    #The reduction in entropy from splitting data into two groups.
    return entropy(y) - (entropy(y_true) * len(y_true) + entropy(y_false) * len(y_false)) / len(y)

def shuffle_samples(a, b):
    #Shuffles two lists of equal length and keeps corresponding elements in the same index.
    rng_state = np.random.get_state()
    #random number generator
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)

