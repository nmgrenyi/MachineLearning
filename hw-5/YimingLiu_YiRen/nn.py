import numpy as np

def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))
def logistic2(x):
    return logistic(x) * (1.0 - logistic(x))

class neuralNetwork:
    def __init__(self, layers):
        # initial weights btw(-0.0001,0.0001)
        self.weights = []
        # input and hidden layers
        for i in range(1, len(layers) - 1):
            r = 0.0002 * np.random.random((layers[i - 1] + 1, layers[i] + 1)) - 0.0001
            self.weights.append(r)
        # output layer
        r = 0.0002 * np.random.random((layers[i] + 1, layers[i + 1])) - 0.0001
        self.weights.append(r)
        #print self.weights


    def fit(self, X, y, alpha=0.1, epochs=5000):
        # add the bias column to the input layer
        ones = np.atleast_2d(np.ones(X.shape[0]))
        X = np.concatenate((ones.T, X), axis=1)
        #forward propagation
        for k in range(epochs):
            i = np.random.randint(X.shape[0])
            a = [X[i]]

            for l in range(len(self.weights)):
                dot = np.dot(a[l], self.weights[l])
                a.append(logistic(dot))

            # output layer
            error = y[i] - a[-1]
            deltas = [error * logistic2(a[-1])]

            #hidden layer
            for l in range(len(a) - 2, 0, -1):

                deltas.append(deltas[-1].dot(self.weights[l].T) * logistic2(a[l]))

            # change locations of hidden and output
            deltas.reverse()

            # back propagation
            for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += alpha * layer.T.dot(delta)

            if k % 100 == 0: print 'epochs:', k

    def predict(self, x):
        a = np.concatenate((np.ones(1).T, np.array(x)), axis=0)
        for l in range(0, len(self.weights)):
            a = logistic(np.dot(a, self.weights[l]))
        return a


if __name__ == '__main__':

    def loadPgm(pgm):
        with open(pgm, 'rb') as f:
            f.readline()  # skip P5
            f.readline()  # skip the comment line
            xs, ys = f.readline().split()  # size of the image
            xs = int(xs)  # 32
            ys = int(ys)  # 30
            max_scale = int(f.readline().strip())
            image = []
            for _ in range(xs * ys):
                image.append(f.read(1)[0])
            image = map(ord, image)
            for i in range(len(image)):
                image[i] = image[i] / float(max_scale)
            return image

    X = []  # 184*960
    y = []  # 184
    Xtest = []  # 83*960
    ytest = []  # 83

    with open('downgesture_train.list') as f:
        for training_image in f.readlines():
            training_image = training_image.strip()
            X.append(loadPgm(training_image))
            if 'down' in training_image:
                y.append(1)
            else:
                y.append(0)

    with open('downgesture_test.list') as f:
        for trainingImage in f.readlines():
            trainingImage = trainingImage.strip()
            Xtest.append(loadPgm(trainingImage))
            if 'down' in trainingImage:
                ytest.append(1)
            else:
                ytest.append(0)

    X = np.array(X)
    y = np.array(y)

    nn = neuralNetwork([960, 100, 960])
    nn.fit(X, y)

    correct = 0.0
    total = 0.0
    p = []

    for e in Xtest:
        if nn.predict(e)[0] * 10 > 3.65:
            p.append(1)
        else:
            p.append(0)

    for i in range(len(p)):
        total += 1
        if p[i] == ytest[i]:
            correct += 1
    print "prediction:" ,p
    print "accuracy:" ,correct/total


