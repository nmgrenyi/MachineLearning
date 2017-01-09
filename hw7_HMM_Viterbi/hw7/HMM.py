import numpy as np
from math import sqrt, log

def loaddata():
	f = open("grid.txt", 'r')
	grid = []
	noisy_distance = []
	for line in f:
		line = line.strip('\n').split(' ')
		line = map(int, line)
		grid.append(line)
	f.close()
	f = open("noisy_distance.txt", 'r')
	for line in f:
		line = line.strip('\n')
		line = str.split(line)
		line = map(float, line)
		noisy_distance.append(line)
	f.close()
	return grid, noisy_distance
	
	
def HMM():
	grid, noisy_distance = loaddata()
	result_grid = np.array(grid)
	domain = []
	#print grid
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == 1:
				domain.append((i, j))
	#print domain
	pai = []
	for _ in domain:
		pai.append(1.0/len(domain))
	#print pai
	A, dict_index_point = getTransMatrix(domain, grid)
	B = getObsProbMatrix(grid, noisy_distance, domain)
	path = viterbi(A, B, pai)
	for i in path:
		result_grid[dict_index_point[i][0]][dict_index_point[i][1]] = 9
		print dict_index_point[i]
	print result_grid
	
	
def getTransMatrix(domain, grid):
	dict_point_index = {}
	dict_index_point = {}
	A = np.zeros((len(domain), len(domain)))
	for i, point in enumerate(domain):
		dict_point_index[point] = i
		dict_index_point[i] = point
	for point_index, point in enumerate(domain):
		neighbourhoods = getNeighber(point, dict_point_index, grid)
		#print neighbourhoods
		for neighbourhood in neighbourhoods:
			A[neighbourhood][point_index] = 1.0/(len(neighbourhoods))
	#print A
	return A, dict_index_point
	
def getNeighber(point, dict_point_index, grid):
	neighbourhoods = []
	if point[0] > 0 and grid[point[0] - 1][point[1]] == 1:
		neighbourhoods.append(dict_point_index[(point[0] - 1, point[1])])
	if point[0] < 9 and grid[point[0] + 1][point[1]] == 1:
		neighbourhoods.append(dict_point_index[(point[0] + 1, point[1])])
	if point[1] > 0 and grid[point[0]][point[1] - 1] == 1:
		neighbourhoods.append(dict_point_index[(point[0], point[1] - 1)])
	if point[1] < 9 and grid[point[0]][point[1] + 1] == 1:
		neighbourhoods.append(dict_point_index[(point[0], point[1] + 1)])
	return neighbourhoods
	
def getObsProbMatrix(grid, noisy_distance, domain):
	res = []
	towers = [[0, 0], [0, 9], [9, 0], [9, 9]]
	for step in noisy_distance:
		record = []
		for point in domain:
			p = 1.0
			for i, tower in enumerate(towers):
				real_distance = sqrt((tower[0] - point[0])**2 + (tower[1] - point[1])**2)
				noisy_distance = [0.7 * real_distance, 1.3* real_distance]
				
				if noisy_distance[0] <= step[i]<= noisy_distance[1]:
					prob = 1.0/(noisy_distance[1] - noisy_distance[0])
				else:
					p = 0.0
					break
				p *= prob
			record.append(p)
		res.append(record)
	#print res
	res = np.mat(res)
	return res

def viterbi(A, B, pai):
	steps = len(B)
	num_domain = len(A)
	delta = np.zeros((steps, num_domain))
	prev = np.zeros((steps, num_domain))
	path = np.zeros(steps)
	for i in range(num_domain):
		delta[0, i] = pai[i] * B[0, i]
		prev[0, i] = 0
	for step in range(steps-1):
		for i in range(num_domain):
			tmp1 = []
			tmp2 = []
			for j in range(num_domain):
				tmp1.append(B[step+1, i] * delta[step, j] * A[j, i])
				tmp2.append(delta[step, j] * A[j, i])
			delta[step+1, i] = max(tmp1)
			tmp2 = np.array(tmp2)
			prev[step + 1, i] = tmp2.argmax()
	prob = max(delta[len(delta) - 1, :])
	path[steps - 1] = delta[len(delta) - 1, :].argmax()
	for step in range(steps - 2, -1, -1):
		path[step] = prev[step + 1, int(path[step + 1])]
	#print delta
	return path	
	
	
if __name__=='__main__':
	HMM()
	