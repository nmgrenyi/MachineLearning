import numpy as np
import matplotlib.pyplot as plt

def loaddata(filename):
	X = []
	Y = []
	f = open(filename, 'r')
	for line in f:
		line_list = line.strip('\r\n').split(',')
		print line_list
		x1 = float(line_list[0])
		x2 = float(line_list[1])
		label = line_list[2]
		X.append([x1 ** 2, x2 ** 2])
		print label
		#Y.append(label)
		#print X
		if label == "+1":
			Y.append('r')
		else:
			Y.append('b')
	X = np.mat(X)
	print X
	print len(Y)
	plt.scatter(X[:, 0], X[:, 1], c=Y, s=50)
	plt.show()
	return X, Y
	
	
if __name__ == '__main__':
	X, Y = loaddata('nonlinsep.txt')