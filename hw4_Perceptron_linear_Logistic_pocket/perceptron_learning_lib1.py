import csv
import numpy as np


def pla_engine(x, W, threshold=0):
    if W.dot(x.T) >= threshold:
        return 1
    else:
        return -1


def learning(X, W, Y, rate=0.01, convergence=1):
        new_W = W
        global_err = 2
        while global_err > convergence:
            global_err = 0
            for index, x in enumerate(X):
                output = pla_engine(x, new_W)
                error = np.array(Y[index] - output)
                new_W += rate * error * x
                global_err += abs(error)
                
#I add this to test wheather there are violate points            
def varify(X, Y, W):
	for i in range(len(X)):
		value = np.dot(W, np.transpose(X[i]))
		if Y[i] == 1 and value < 0:
			print "Y[i] == 1 and value < 0"
		elif Y[i] == -1 and value >= 0:
			print "Y[i] == -1 and value >= 0"

data = []
with open('classification.txt') as csvfile:
    points = csv.reader(csvfile, delimiter=',')
    for point_str in points:
        data.append(point_str)

data = np.array(data).astype(np.float)
#print (data)
data = np.delete(data, np.s_[4:5], axis=1)
#print (data)
X = np.delete(data, np.s_[3:4], axis=1)
#print X
X = np.append(X, (np.zeros(len(X)) + 1).T.reshape(len(X), 1), axis=1)
#print X
Y = np.delete(data, np.s_[0:3], axis=1).squeeze()
#print Y

W = np.zeros(X[0].shape[0])
#print W

learning(X, W, Y)
varify(X, Y, W)

print W
