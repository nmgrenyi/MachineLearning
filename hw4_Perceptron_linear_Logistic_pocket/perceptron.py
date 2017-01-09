'''
created by Yi Ren & Yiming Liu
'''
import csv
import numpy as np
from random import choice
#import matplotlib.pyplot as plt
	
	
def perceptron(X, Y, W):
	aierfa = 0.01
	#num_of_mis_point = []
	#mis_list = []
	hasFalse = True
	itr = 0
	while hasFalse:
		itr += 1
		mis_list = [ ]
		hasFalse = False
		for i in range(len(X)):
			value = np.dot(W, np.transpose(X[i]))
			if Y[i] == 1 and value < 0:
				mis_list.append(i)
			elif Y[i] == -1 and value >= 0:
				mis_list.append(i)
		#print "number of mis_point: ", len(mis_list)
		#num_of_mis_point.append(len(mis_list))
		if len(mis_list) >= 1:
			hasFalse = True
			mis_classification_point = choice(mis_list)
			value = np.dot(W, np.transpose(X[mis_classification_point]))
			if Y[mis_classification_point] == 1 and value < 0:
				W = W + aierfa * np.transpose(X[mis_classification_point])
			elif Y[mis_classification_point] == -1 and value >= 0:
				W = W - aierfa * np.transpose(X[mis_classification_point])

	print "result w: ", W
	#print itr
	#plt.plot(num_of_mis_point)
	#plt.show()
	return W
	
	
	
def varify(X, Y, new_W):
	#try_W = np.array([0, 3.57296995, -2.76416441, -2.17957628]) this is used for this library
	#print (try_W)
	for i in range(len(X)):
		value = np.dot(new_W, np.transpose(X[i]))
		if Y[i] == 1 and value < 0:
			print "Y[i] == 1 and value < 0"
		elif Y[i] == -1 and value >= 0:
			print "Y[i] == -1 and value >= 0"
		
		


def loaddata(filename):
    data = []
    f = open(filename)
    lines = csv.reader(f, delimiter=',')
    for line in lines:
        numbers = []
        for num in line:
            numbers.append(float(num))
        data.append(numbers)
    data = np.array(data)
    X = np.array([x[0:3] for x in data])
    X = np.c_[np.ones((len(X), 1)), X]
    Y = np.array([x[3:4] for x in data])
    W = np.zeros(len(X[0]))
    return X, Y, W

if __name__ == '__main__':
    X, Y, W = loaddata("classification.txt")
    new_W = perceptron(X, Y, W)
    varify(X, Y, new_W)
