'''
made by Yi Ren for INF 552, 2016fall

python 2.7.11
'''

import numpy as np
import random
import math
import matplotlib.pyplot as plt

def EM_GMM(filename, K):
    #get data, dimension, and number of points
    data = []
    f = open(filename)
    for line in f:
        line_list = line.strip('\n').strip('\r').split(',')
        number_line_list = []
        for string in line_list:
            number_line_list.append(float(string))
        data.append(number_line_list)
    f.close()
    data_matrix = np.mat(data)
    number_of_point = len(data)
    if number_of_point < K:
        print "the number of points is small than the number of clusters"
    dimension = len(data[0])
    if dimension < 0:
        print "wrong point!"
    
    #initialize miu
    miu_cluster = random.sample(data_matrix, K)
    #print miu_cluster
    
    #initialize pi_cluster and sigma_cluster
    #assigin each points to one cluster
    distance_matrix = np.zeros((number_of_point, K))
    for cluster_number in range(K):
        X = data_matrix - miu_cluster[cluster_number]
        for n in range(number_of_point):
            distance_matrix[n, cluster_number : (cluster_number+1)] = np.sum(np.power(X, 2), 1)[n, 0]
    min_distance = np.argmin(distance_matrix, axis = 1)
    #print min_distance
    pi_cluster = np.zeros((1, K))
    sigma_cluster = np.zeros((dimension, dimension, K))
    for cluster_number in range(K):
        index_of_cluster = []
        for n in range(number_of_point):
            if min_distance[n] == cluster_number:
                index_of_cluster.append(n)
        sigma_cluster[:, :, cluster_number] = np.cov(np.transpose(data_matrix[index_of_cluster, :]))
        pi_cluster[0, cluster_number] = float(len(index_of_cluster)) / number_of_point
    #print ("Ini_pi")
    #print pi_cluster
    threshold = 0.00001
    Lprev = -1000.0
    global constant 
    constant = math.pow(2*math.pi, -dimension/2)
    #print constant

    while True:
        #Estimation-step
        r = np.zeros((number_of_point, K))
        prob = calculate_probility(data_matrix, number_of_point, dimension, miu_cluster, sigma_cluster, K)
        for n in range(number_of_point):
            sum_value = 0
            #calculate denominator of r(i,c):
            for cluster_number in range(K):
                sum_value += pi_cluster[0, cluster_number] * prob[n, cluster_number]
            for cluster_number in range(K):
                r[n, cluster_number] = pi_cluster[0, cluster_number] * prob[n, cluster_number]/sum_value
        #print (r)
        
        #Maximization-step
        #update pi_cluster
        miu_f = np.sum(r, 0)#the sum of prob of each point generate by No.k cluster
        pi_cluster = np.mat([miu_f / number_of_point])

        #update miu_cluster
        miu_cluster = np.zeros((K, dimension))
        tmp_sum_of_new_distr = np.zeros((1, dimension))
        for cluster_number in range(K):
            tmp_sum_of_new_distr = np.transpose(r)[cluster_number,:] * data_matrix
            miu_cluster[cluster_number,:] = tmp_sum_of_new_distr
        for cluster_number in range(K):
            miu_cluster[cluster_number] = miu_cluster[cluster_number] / miu_f[cluster_number]

        #update sigma_cluster
        for cluster_number in range(K):
            tmp_point_sigma = np.zeros((dimension, dimension))
            X = data_matrix - miu_cluster[cluster_number]
            for n in range(number_of_point):
                #print (np.transpose(X[i]) * X[i])
                tmp_point_sigma += r[n][cluster_number] * (np.transpose(X[n]) * X[n])
            sigma_cluster[:, :, cluster_number] = tmp_point_sigma / miu_f[cluster_number]

        #check convergence:
        Log_likelihood_function = np.sum(np.log(prob*(np.transpose(pi_cluster))))
        if Log_likelihood_function - Lprev < threshold:
            print "mean: "
            print miu_cluster, '\n'
            print "amplitude"
            print pi_cluster, '\n'
            print "covariance matrix"
            for k in range(K):
                print sigma_cluster[:,:, k]
            break
        Lprev = Log_likelihood_function

    #plot
    max_prob_index = np.argmax(prob, axis = 1)
    for cluster_number in range(K):
        points = []
        for n in range(number_of_point):
            if max_prob_index[n] == cluster_number:
                points.append(data[n])
        for point in points:
            if cluster_number == 0:
                plt.scatter(point[0], point[1], color = 'red')
            elif cluster_number == 1:
                plt.scatter(point[0], point[1], color = 'yellow')
            elif cluster_number == 2:
                plt.scatter(point[0], point[1], color = 'green')
            elif cluster_number == 3: #in case of more input clusters
                plt.scatter(point[0], point[1], color = 'blue')
            elif cluster_number == 4:
                plt.scatter(point[0], point[1], color = 'orange')
    plt.show()

#calculate Gaussian Distribution for each point:
def calculate_probility(data_matrix, number_of_point, dimension, miu, sigma, K):
    prob = np.zeros((number_of_point, K))
    for cluster_number in range(K):
        X_minus_miu = (data_matrix) - np.tile(miu[cluster_number], (number_of_point, 1))
        sigma_determinant = np.linalg.det(sigma[:, :, cluster_number])
        #print sigma_determinant
        inverse_sigma = np.linalg.inv(sigma[:, :, cluster_number])
        #print inverse_sigma
        cluster_det = math.pow(sigma_determinant, -0.5)
        #print tmp_det

        for n in range(number_of_point):
            tmp = -0.5 * X_minus_miu[n, :] * inverse_sigma * np.transpose(X_minus_miu[n, :])
            prob[n, cluster_number] = constant * cluster_det * math.exp(tmp) # I can put constant to the outter loop to save CPU, but it is easy for human to understand if I put it in loop
    #print sum(prob[:,0])
    return prob
        
if __name__ == '__main__':
    
    EM_GMM("clusters.txt", 3)
