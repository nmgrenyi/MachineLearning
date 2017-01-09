import numpy as np
import cvxopt
import cvxopt.solvers
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
		X.append([x1, x2])
		Y.append(label)
	return X, Y

def svm(X, Y):
	X = np.mat(X)
	number_of_points, dimension = X.shape
	tmp = np.zeros((number_of_points, number_of_points))
	for i in range(number_of_points):
		for j in range(number_of_points):
			Y_val = Y[i] * Y[j]
			tmp[i, j] = Y_val * np.dot(X[i], np.transpose(X[j]))
	
	P = cvxopt.matrix(tmp)
	q = cvxopt.matrix(np.ones(number_of_points) * -1)
	A = cvxopt.matrix(Y, (1, number_of_points))
	b = cvxopt.matrix(0.0)
	G = cvxopt.matrix(np.diag(np.ones(number_of_points) * -1))
	h = cvxopt.matrix(np.zeros(number_of_points))
	solution = cvxopt.solvers.qp(P, q, G, h, A, b)
	a = np.ravel(solution['x'])
	aierfa = []
	aierfa_index = []
	for i in range(len(a)):
		if a[i] > 1e-3:
			aierfa.append(1)
			aierfa_index.append(i)
		else:
			aierfa.append(0)
	w = np.zeros(2)
	Y = np.mat(Y)
	Y = np.squeeze(np.asarray(Y))
	for i in aierfa_index:
		w += (a[i] * Y[i]) * np.squeeze(np.asarray(X[i]))
	w = np.squeeze(np.asarray(w))
	slope = -w[0]/w[1]
	for i in range(len(aierfa_index)):
		print X[i]
		b = 1.0/Y[aierfa_index[i]] - w * np.transpose(X[aierfa_index[i]])
	b = np.squeeze(np.asarray(b))
	print "b: ", b
	x = np.linspace(-0.2, 1.2)
	y = slope * x - (b) / w[1]
	
	b_down = X[aierfa_index[0]]
	b_down = np.squeeze(np.asarray(b_down))
	y_down = slope* x + (b_down[1] - slope * b_down[0])
	b_up = X[aierfa_index[2]]
	b_up = np.squeeze(np.asarray(b_up))
	y_up = slope * x + (b_up[1] - slope * b_up[0])
	
	plt.plot(x, y, '-')
	plt.plot(x, y_down, '--')
	plt.plot(x, y_up, '--')
	plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
	
	plt.show()

if __name__ == '__main__':
	X, Y = loaddata('linsep.txt')
	svm(X, Y)
		
		