'''
created by Yi Ren & Yiming Liu
'''
import csv
import numpy as np
from random import choice
import matplotlib.pyplot as plt


def pocket(X, Y, W):
	aierfa = 0.001
	hasFalse = True
	itr = 0
	while hasFalse and itr < 8000:
		itr = itr + 1
		if itr % 1000 == 0:
			print "itrition times: ", itr
		hasFalse = False
		for i in range(len(X)):
			value = np.dot(W, np.transpose(X[i]))
			if Y[i] == 1 and value < 0:
				W = W + aierfa * np.transpose(X[i])
				hasFalse = True
			elif Y[i] == -1 and value >= 0:
				W = W - aierfa * np.transpose(X[i])
				hasFalse = True
	print W
	return W
	
	
def pocket_after(X, Y, W):
	new_W = np.zeros(len(X[0]))
	min_num_of_mis_points = len(X)
	aierfa = 0.01
	seq_of_num_of_misclassified_points = []
	hasFalse = True
	itr = 0
	while hasFalse and itr < 7000:
		itr += 1
		if itr %1000 == 0:
			print itr
		hasFalse = False
		#detect violate points and put them input mis_list
		mis_list = [ ]
		for i in range(len(X)):
			value = np.dot(W, np.transpose(X[i]))
			if Y[i] == 1 and value < 0:
				mis_list.append(i)
			elif Y[i] == -1 and value >= 0:
				mis_list.append(i)
		#v1 = len(mis_list)
		if itr == 1:
			min_num_of_mis_points = len(mis_list)
			seq_of_num_of_misclassified_points.append(len(mis_list))
		if len(mis_list) < 1:#if all constraints are satisified
			hasFalse = False
			min_num_of_mis_points = 0
		elif len(mis_list) >= 1:
			v1 = len(mis_list) #count number of violate points before
			hasFalse = True
			#pick up a random violate
			mis_classification_point = choice(mis_list)
			value = np.dot(W, np.transpose(X[mis_classification_point]))
			if Y[mis_classification_point] == 1 and value < 0:
				W = W + aierfa * np.transpose(X[mis_classification_point])
			elif Y[mis_classification_point] == -1 and value >= 0:
				W = W - aierfa * np.transpose(X[mis_classification_point])
			mis_list = []
			#count number of violate points after
			for j in range(len(X)):
				value = np.dot(W, np.transpose(X[j]))
				if Y[j] == 1 and value < 0:
					mis_list.append(j)
				elif Y[j] == -1 and value >= 0:
					mis_list.append(j)
			v2 = len(mis_list)
			if v2 == 0: #no violate points when use new_W
				hasFalse = False
			print v1, v2
			#print "v2: ", v2
			if v2 < v1 and v2 < min_num_of_mis_points:
				best_W = W
				min_num_of_mis_points = v2
				seq_of_num_of_misclassified_points.append(v2)
			else:
				#W = new_W
				seq_of_num_of_misclassified_points.append(v1)

	print best_W
	print "seq_of_num_of_misclassified_points: ", len(seq_of_num_of_misclassified_points)
	plt.plot(seq_of_num_of_misclassified_points)
	plt.show()
	return best_W
		
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
    new_W = pocket_after(X, Y, W)
    varify(X, Y, new_W)
