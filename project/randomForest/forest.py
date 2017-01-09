from __future__ import division
import numpy as np
from scipy.stats import mode
from tools import shuffle_samples
from tree import DecisionTreeClassifier


class RandomForestClassifier(object):

    def __init__(self, n_estimators=30, max_features=np.sqrt, max_depth=10,
                 min_samples_split=2, bootstrap=0.9):
        """
        Arguments:
            n_estimators: The number of decision trees in the random forest.
            max_features: Controls the number of features to randomly consider
                at each split.
            max_depth: The maximum number of levels that the tree can grow
                downwards before forcefully becoming a leaf.
            min_samples_split: The minimum number of samples needed at a node to
                justify a new node split.
            bootstrap: A part of randomly chosen data to fit each tree on.
        """
        self.num_estimators = n_estimators
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.bootstrap = bootstrap
        self.forest = []

    def fit(self, X, y):
        #Generate a forest by a random subset of data and features.
        self.forest = []
        n_samples = len(y)
        n_sub_samples = round(n_samples * self.bootstrap)

        for i in xrange(self.num_estimators):
            shuffle_samples(X, y)
            X_subset = X[:n_sub_samples]
            y_subset = y[:n_sub_samples]

            tree = DecisionTreeClassifier(self.max_features, self.max_depth,
                                          self.min_samples_split)
            tree.fit(X_subset, y_subset)
            self.forest.append(tree)

    def predict(self, X):
        #Predict the class of each sample in X.
        n_samples = X.shape[0]
        n_trees = len(self.forest)
        predictions = np.empty([n_trees, n_samples])
        for i in xrange(n_trees):
            predictions[i] = self.forest[i].predict(X)
        #print predictions
        return mode(predictions)[0][0]

    def score(self, X, y):
        #Return the accuracy of the prediction of X compared to y.
        y_predict = self.predict(X)
        n_samples = len(y)
        correct = 0
        for i in xrange(n_samples):
            if y_predict[i] == y[i]:
                correct = correct + 1
        accuracy = correct / n_samples
        return accuracy


from sklearn.datasets import load_digits
from sklearn import cross_validation
import numpy as np


digits = load_digits(n_class = 10)
X = digits.data
y = digits.target
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y)
print "X",X_train[0]
print "y",y
forest = RandomForestClassifier()
forest.fit(X_train, y_train)

accuracy = forest.score(X_test, y_test)
print 'The accuracy was', accuracy, ' on the test data.'

classifications = forest.predict(X_test)
print 'The digit at index 1 of X_test was classified as a', classifications[1], '.'


