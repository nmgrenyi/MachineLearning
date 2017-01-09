import numpy as np
import sklearn
from sklearn import svm
import matplotlib.pyplot as plt

def loaddata(filename):
	X = []
	Y = []
	f = open(filename, 'r')
	for line in f:
		line_list = line.strip('\r\n').split(',')
		x1 = float(line_list[0])
		x2 = float(line_list[1])
		label = float(line_list[2])
		X.append([x1 ** 2, x2 ** 2])
		Y.append(label)
	return X, Y

def svm(X, Y):
	X = np.mat(X)
	clf = sklearn.svm.SVC(kernel = 'linear')
	clf.fit(X, Y)
	w = clf.coef_[0]
	slope = -w[0]/w[1]
	x = np.linspace(0, 200)
	y = slope * x - (clf.intercept_[0]) / w[1]
	
	b_down = clf.support_vectors_[0]
	b_down = np.squeeze(np.asarray(b_down))
	y_down = slope* x + (b_down[1] - slope * b_down[0])
	b_up = clf.support_vectors_[1]
	b_up = np.squeeze(np.asarray(b_up))
	y_up = slope * x + (b_up[1] - slope * b_up[0])
	
	plt.plot(x, y, '-')
	plt.plot(x, y_down, '--')
	plt.plot(x, y_up, '--')
	plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
	
	plt.show()

	
if __name__ == '__main__':
	X, Y = loaddata('nonlinsep.txt')
	svm(X, Y)
		
		
