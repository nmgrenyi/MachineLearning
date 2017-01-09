import numpy as np
import cvxopt
import cvxopt.solvers
import matplotlib.pyplot as plt

def loaddata(filename):
	X = []
	Y = []
	f = open(filename, 'r')
	for line in f:
		line_list = line.split(' ')
		x1 = float(line_list[0])
		x2 = float(line_list[1])
		label = float(line_list[2])
		X.append([x1 ** 2, x2 ** 2])
		Y.append(label)
	return X, Y

def svm(X, Y):
	X = np.mat(X)
	#Y = np.mat(Y)
	#print X
	number_of_points, dimension = X.shape
	K = np.zeros((number_of_points, number_of_points))
	tmp = np.zeros((number_of_points, number_of_points))
	for i in range(number_of_points):
		for j in range(number_of_points):
			Y_val = Y[i] * Y[j]
			K[i, j] = np.dot(X[i], np.transpose(X[j]))
			tmp[i, j] = Y_val * np.dot(X[i], np.transpose(X[j]))
	
	P = cvxopt.matrix(tmp)
	q = cvxopt.matrix(np.ones(number_of_points) * -1)
	A = cvxopt.matrix(Y, (1, number_of_points))
	#print A
	b = cvxopt.matrix(0.0)
	G = cvxopt.matrix(np.diag(np.ones(number_of_points) * -1))
	h = cvxopt.matrix(np.zeros(number_of_points))
	#print h
	
	solution = cvxopt.solvers.qp(P, q, G, h, A, b)
	#a = solution['x']
	a = np.ravel(solution['x'])
	print solution['primal objective']
	print a
	aierfa = []
	aierfa_index = []
	for i in range(len(a)):
		if a[i] > 1e-5:
			aierfa.append(1)
			aierfa_index.append(i)
		else:
			aierfa.append(0)
	w = np.zeros(2)
	Y = np.mat(Y)
	Y = np.squeeze(np.asarray(Y))
	print Y
	for i in aierfa_index:
		print X[i]
		w += (a[i] * Y[i]) * np.squeeze(np.asarray(X[i]))
		#w = w + aierfa[i] * a[i] * X[i]
	w = np.squeeze(np.asarray(w))
	print w
	slope = -w[0]/w[1]
	print slope
	print aierfa_index
	for i in range(len(aierfa_index)):
		b = 1.0/Y[aierfa_index[i]] - w * np.transpose(X[aierfa_index[i]])
	b = np.squeeze(np.asarray(b))
	print b
	xx = np.linspace(0, 200)
	yy = slope * xx - (b) / w[1]
	
	b = X[aierfa_index[0]]
	b = np.squeeze(np.asarray(b))
	print b
	yy_down = slope* xx + (b[1] - slope * b[0])
	b = X[aierfa_index[2]]
	b = np.squeeze(np.asarray(b))
	yy_up = slope * xx + (b[1] - slope * b[0])
	
	plt.plot(xx, yy, 'k-')
	plt.plot(xx, yy_down, 'k--')
	plt.plot(xx, yy_up, 'k--')
	plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)
	
	plt.show()
	
	
'''
	sv = a > 1e-5
	ind = np.arange(len(a))[sv]
	print sv
	print ind
	selfa = a[ind]
	print selfa
	selfsv = X[sv]
	print selfsv
	selfsv_y = Y[sv]
	print selfsv_y
	print "%d support vectors out of %d points" % (len(selfa), number_of_points)
	selfb = 0
	for n in range(len(selfa)):
		selfb += selfsv_y[n]
		selfb -= np.sum(selfa * selfsv_y * K[ind[n], sv])
	selfb /= len(selfa)
	print selfb
'''
	
		
	
	
if __name__ == '__main__':
	X, Y = loaddata('nnsvm-data.txt')
	svm(X, Y)
		
		