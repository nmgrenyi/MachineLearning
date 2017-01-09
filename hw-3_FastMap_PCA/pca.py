#Principal Component Analysis (PCA)
#@Yiming Liu @Ren Yi
import numpy as np
from numpy import linalg as LA

def pca(X,k):
    #K: number of components to keep
   #number of data, dimension
  dataNum, dim = X.shape
  print X.shape
  mean = np.array([np.mean(X[:,i]) for i in range(dim)])

  #Caculate the covariance matrix
  covM = (X - mean).T.dot((X - mean)) / (X.shape[0] - 1)

  # calculate  eigenvalues and eigenvectors
  eigVal, eigVec = LA.eig(covM)
  eigGroup = [(eigVal[i], eigVec[:,i]) for i in range(dim)]

  # based on eigValue, arrange eigVector from highest to lowest
  #the top eigvectors's direction keep the most information of the original matrix
  eigGroup.sort(reverse = True)

  # choose the top k eigVectors
  topEigVec = np.array([e[1] for e in eigGroup[:k]])

  # output the directions of the first two principal components
  print "Top 2 principal components' vectors:\n" ,topEigVec

  newX = np.dot(X - mean,np.transpose(topEigVec))
  return newX

if __name__ == '__main__':
    X = np.loadtxt('pca_data.txt')

    print pca(X,2)
    #print pca(X,2).shape

