'''
created by Yi Ren & Yiming Liu
'''
import csv
import numpy as np
from random import choice
import matplotlib.pyplot as plt
	
	
def pocket(X, Y, W):
	seq_of_num_of_mis_point = []
	best_W = W
	length_of_shortest_mis_list = len(X)
	aierfa = 0.01
	itr = 0
	hasFalse = True
	while hasFalse and itr < 7000:
		itr = itr + 1
		#if itr % 1000 == 0:
		#	print "itrition times: ", itr
		mis_list = [ ]
		hasFalse = False
		for i in range(len(X)):
			value = np.dot(W, np.transpose(X[i]))
			if Y[i] == 1 and value < 0:
				mis_list.append(i)
			elif Y[i] == -1 and value >= 0:
				mis_list.append(i)
		#seq_of_num_of_mis_point.append(len(mis_list))
		if len(mis_list) >= 1:
			hasFalse = True
			if len(mis_list) < length_of_shortest_mis_list:
				best_W = W
				length_of_shortest_mis_list = len(mis_list)
			seq_of_num_of_mis_point.append(len(mis_list))
		#random find a misclassified point, and calculate the new W
			mis_classification_point = choice(mis_list)
			value = np.dot(W, np.transpose(X[mis_classification_point]))
			if Y[mis_classification_point] == 1 and value < 0:
				W = W + aierfa * np.transpose(X[mis_classification_point])
			elif Y[mis_classification_point] == -1 and value >= 0:
				W = W - aierfa * np.transpose(X[mis_classification_point])
	print "best W; ", best_W
	plt.plot(seq_of_num_of_mis_point)
	plt.show()
	return best_W
	
#calculate how many violate points in the end
def varify(X, Y, new_W):
	print ("length of data", len(X))
	countY1 = 0
	countYm1 = 0
	for i in range(len(X)):
		value = np.dot(new_W, np.transpose(X[i]))
		if Y[i] == 1 and value < 0:
			#print "Y[i] == 1 and value < 0"
			countY1 += 1
		elif Y[i] == -1 and value >= 0:
			#print "Y[i] == -1 and value >= 0"
			countYm1 += 1
	print ("Y = +1 but value < 0", countY1)
	print ("Y = -1 but value >= 0", countYm1)
		
		


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
    Y = np.array([x[4:5] for x in data])
    W = np.zeros(len(X[0]))
    return X, Y, W

if __name__ == '__main__':
    X, Y, W = loaddata("classification.txt")
    new_W = pocket(X, Y, W)
    #varify(X, Y, new_W)
