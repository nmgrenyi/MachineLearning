'''

created by Yi Ren & Yiming Liu for INF552

Python 2.7.11

'''

import numpy as np
import matplotlib.pyplot as plt

def fastmap(filename, dimension):
    dis_mat, num_of_points = loaddata(filename)
    iterition = dimension
    res = []
    while iterition > 0:
        iterition -= 1
        farest_pair, far_dis = farestPair(dis_mat)
        a = farest_pair[0]
        b = farest_pair[1]
        X = []
        for i in range(num_of_points):
            x  = (dis_mat[a,i]**2 + far_dis**2 - dis_mat[b, i]**2) / (2*far_dis)
            X.append(x)
        res.append(X)
        new_dis_mat = np.zeros((num_of_points, num_of_points))
        for i in range(num_of_points):
            for j in range(num_of_points):
                new_dis_mat[i][j] = np.sqrt(dis_mat[i][j]**2 - (X[i] - X[j])**2)
        dis_mat = new_dis_mat
    
    print np.mat(res)
    n = ['acting', 'activist',
'compute', 'coward',
'forward',
'interaction',
'activity',
'odor',
'order',
'international']
    fig, ax = plt.subplots()
    ax.scatter(res[0],res[1])
    for i, txt in enumerate(n):
        ax.annotate(txt, (res[0][i], res[1][i]))
    plt.show()


def loaddata(filename):
    #input data
    data_file = []
    f = open(filename)
    for line in f:
        line_list = line.split()
        line_inf = []
        for c in line_list:
            line_inf.append(int(c))
        data_file.append(line_inf)
    length = len(data_file)
    #make distance matrix
    sum_val = 0
    i = 1
    while True:
        sum_val += i
        i += 1
        if sum_val == length:
            break
    data = np.zeros((i, i))
    for dis in data_file:
        data[dis[0]-1][dis[1]-1] = dis[2]
        data[dis[1]-1][dis[0]-1] = dis[2]
    return data, i

#find the farthest pair of points
def farestPair(data_mat):
    max_val = np.amax(data_mat)
    far_pair = []
    for i in range(len(data_mat)):
        for j in range(len(data_mat[i])):
            if data_mat[i][j] == max_val:
                far_pair.append(i)
                far_pair.append(j)
                return far_pair, max_val
   


if __name__ == '__main__':
    fastmap("fastmap-data.txt", 2)
