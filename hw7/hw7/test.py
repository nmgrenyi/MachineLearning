import math

X = [4, 5, 6, 7, 7, 7, 7, 6, 5, 4, 3]
Y = [4, 4, 4, 4, 3, 2, 1, 1, 1, 1, 1]

for i in range(11):
	dis_0 = math.sqrt(X[i] ** 2 + Y[i]**2)
	dis_1 = math.sqrt((X[i] - 0)** 2 + (Y[i] - 9)**2)
	dis_2 = math.sqrt((X[i] - 9)** 2 + (Y[i] - 0)**2)
	dis_3 = math.sqrt((X[i] - 9)** 2 + (Y[i] - 9)**2)
	print dis_1*0.7, dis_1*1.3