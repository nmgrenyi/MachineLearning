import numpy as np
from numpy import *
from numpy.linalg import inv

data = np.loadtxt("linear-regression.txt", delimiter=',')
m,n = data.shape
x1 = ones(m).T

X = mat(data[:, :2])

X = np.c_[x1,X]

Y = mat(data[:, 2])
print Y
Y = Y.T


weight = np.dot(np.dot(np.dot(X.T,X).I,X.T),Y)

print weight
