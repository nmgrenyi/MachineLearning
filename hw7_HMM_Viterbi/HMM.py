import numpy as np
from math import sqrt, log

def loaddata():
	f = open("hmm-data.txt", 'r')
	grid = []
	tower = []
	noisy_distance = []
	line_no = 0
	for line in f:
		if line_no >= 2 and line_no <= 11:
			line = line.strip('\n').split(' ')
			line = map(int, line)
			grid.append(line)
		elif line_no >= 16 and line_no <= 19:
			tower.append([int(line[9]), int(line[11])])
		elif line_no >= 24:
			line = line.strip('\n').split(' ')
			line = map(float, line)
			noisy_distance.append(line)
		line_no += 1
	f.close()
	return grid, tower, noisy_distance
	
	
if __name__=='__main__':
	grid, tower, noisy_distance = loaddata()
	grid = np.mat(grid)
	noisy_distance = np.mat(noisy_distance)
	print noisy_distance
	next_positions = []
	for x in range(len(grid)):
		for y in range(len(grid[0])):
			next_positions.append([x, y])
	for step in noisy_distance:
		highest_prob_cell = [0, 0, -1000]
		for next_pos in next_positions:
			p = (1./len(next_positions)) * cur_pos_prob()
			if p == 0:
				continue
			else:
				if p > highest_prob_cell[2]:
					highest_prob_cell[next_pos[0], next_pos[1], p]
		print (hight_prob_cell[])
	