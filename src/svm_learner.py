import numpy as np
import mlpy
import os
import matplotlib.pyplot as plt

TRAIN_PERC = 0.9

def main():
    #Load the game data from file
    #game_data.txt, comma delimited
    path = os.path.join('..', 'samples', 'sample_data.txt')
    gdata = np.loadtxt(path, delimiter=',')

    w = gdata.shape[0]
    x, y = gdata[:, :w], gdata[:, w].astype(np.int)

    
    train_data, test_data = sample(TRAIN_PERC, gdata)

    train_x, train_y = train_data[:, :w], train_data[:, w].astype(np.int)
    test_x, test_y = test_data[:, :w], test_data[:, w].astype(np.int)

    #Dimensionality reduction
    pca = mlpy.PCA()
    pca.learn(train_x)
    train_z = pca.transform(train_x, k=2)

    #Plot stuff (principle components)
    plt.set_cmap(plt.cm.Paired)
    fig1 = plt.figure(1)
    title = plt.title("PCA on iris dataset")
    plot = plt.scatter(train_z[:, 0], train_z[:, 1], c=train_y)
    labx = plt.xlabel("First component")
    laby = plt.ylabel("Second component")
    plt.show()
    

def sample(percent, data):
    '''percent of data to become training data'''
    #Get the size (rows) of the data set
    n = data.shape[0]

    '''
    indices = list(xrange(len))
    #Randomly select tr points (without replacement) from indices
    tr_i = indices[np.random.choice(n, tr), replace=False]
    #take the remaining indices and place them in our test index list
    ts_i = [val for val in indices if val not in tr_i]

    #separate our data into training and testing sets
    tr_data = data[tr_i]
    ts_data = data[ts_i]

    return (tr_data, ts_data)'''
    tr = n * percent
    ts = n - tr

    np.random.shuffle(data)
    training_data = data[:tr]
    testing_data = data[ts:]
    return (training_data, testing_data)

if __name__ == '__main__':
    main()