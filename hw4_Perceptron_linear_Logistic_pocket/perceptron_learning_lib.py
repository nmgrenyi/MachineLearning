import numpy as np
import csv


class Perceptron(object):

    def __init__(self, eta=0.01, n_iter=1000):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        print self.w_
        return self

    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)
        
        
        
        
data = []
f = open("classification.txt")
lines = csv.reader(f, delimiter=',')
for line in lines:
    numbers = []
    for num in line:
        numbers.append(float(num))
	data.append(numbers)
f.close()
data = np.array(data)
X = np.array([x[0:3] for x in data])
y = np.array([x[3:4] for x in data])     
        
ppn = Perceptron(eta=0.1, n_iter=15)

ppn.fit(X, y)

