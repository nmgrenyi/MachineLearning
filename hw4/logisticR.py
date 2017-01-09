import numpy as np
from numpy import *
import pandas as pd
data = np.loadtxt("classification.txt",delimiter=',')
m,n = data.shape
x1 = ones(m).T
X = data[:,0:3]
X = np.c_[x1,X]
Y = data[:,4]

for i in range(0,m):
    Y[i]=(Y[i]+1)/2

Y = Y.reshape(len(data), 1)

def sigmoidFunction(x):
    result = 1.0 / (1 + exp(-x))
    return result

# 1/(1+e*(-(y*wT*x)))
#set loop times
maxTimes = 500
m,n = X.shape
weight = np.zeros((n,1))
#initial cost function
cost = pd.Series(np.arange(maxTimes, dtype= float))
#set learning rate
rate =  0.001

for i in range(0,maxTimes):
   h = sigmoidFunction(np.dot(X,weight))
   cost[i] = -(1/m)*np.sum(Y*np.log(h)+(1-Y)*np.log(1-h))
   error = h - Y
   gradientDescent = np.dot(X.T, error)
   weight -= rate * gradientDescent

print weight


