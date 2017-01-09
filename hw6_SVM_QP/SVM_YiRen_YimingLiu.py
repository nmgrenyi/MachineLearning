import numpy as np
import cvxopt
import cvxopt.solvers

def loaddata(filename):
	X = []
	Y = []
	f = open(filename, 'r')
	for line in f:
		line_list = line.split(',')
		x1 = float(line_list[0])
		x2 = float(line_list[1])
		label = int(line_list[2])
		X.append([x1, x2])
		Y.append(label)
	print X
	print Y
	
	
	
if __name__ == '__main__':
	data	= loaddata('linesep.txt')
		
		