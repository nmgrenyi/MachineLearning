'''
made by Yi Ren for INF552, 2016fall

python 2.7.11
'''

import numpy as np
import random
import math
import copy
import matplotlib.pyplot as plt

def K_MEANS(filename, K):
    data = []
    f = open(filename)
    for line in f:
        line_list = line.strip('\n').strip('\r').split(',')
        number_line_list = []
        for string in line_list:
            number_line_list.append(float(string))
        data.append(number_line_list)
    f.close()
    number_of_point = len(data)
    dimension = len(data[0])

    #print data
    centroid = []
    for k in range(K):
        centroid.append(data[random.randint(0, number_of_point)])
    #print "centroid_random"
    #print centroid

    while True:
        #get points in each cluster
        cluster = []
        for k in range(K):
            cluster.append([])
        #print cluster
        for i in range(number_of_point):
            distance_to_cluster = []
            for k in range(K):
                distance_to_cluster.append(get_distance(data[i], centroid[k]))
                #print np.argmin(distance_to_cluster)
            cluster[np.argmin(distance_to_cluster)].append(i)
        #print cluster
        old_centroid = copy.deepcopy(centroid)

        #calculate new centroid
#        new_centroid = []
        for k in range(K):
            for d in range(dimension):
                sum_val = 0
                for i in cluster[k]:
                    sum_val += data[i][d]
                centroid[k][d] = sum_val / len(cluster[k])

        #compare old_centroid and centroid
        if old_centroid == centroid:
            break
    #print centroid

    for k in range(K):
        points = []
        for point_index in cluster[k]:
            points.append(data[point_index])
        #print points
        for point in points:
            if k == 0:
                plt.scatter(point[0], point[1], color = 'red')
            elif k == 1:
                plt.scatter(point[0], point[1], color = 'yellow')
            elif k == 2:
                plt.scatter(point[0], point[1], color = 'green')
            elif k == 3:
                plt.scatter(point[0], point[1], color = 'blue')
            elif k == 4:
                plt.scatter(point[0], point[1], color = 'orange')
    print "the three centroids are: "
    print centroid
    plt.show()
    
def get_distance(data_point, centroid):
    dimension = len(data_point)
    distance_sqrt = 0
    for d in range(dimension):
        distance_sqrt += (data_point[d] - centroid[d])**2
    distance = math.sqrt(distance_sqrt)
    return distance


if __name__ == '__main__':
    
    K_MEANS("clusters.txt", 3)
