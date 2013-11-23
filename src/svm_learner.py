import numpy as np
import mlpy

TRAIN_PERC = 0.9

def main():
    #Load the game data from file
    #game_data.txt, comma delimited
    
    gdata = np.loadtxt('sample_data.txt', delimiter=',')
    w = gdata.width
    x, y = gdata[:, :w], gdata[:, w].astype(np.int)
    x.shape
    y.shape
    
    train_data, test_data = sample(TRAIN_PERC, gdata)
    #Dimensionality reduction
    pca = mlpy.PCA()
    


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
    tr = size * percent
    ts = size - tr

    np.shuffle(data)
    training_data = data[:tr]
    testing_data = data[ts:]
    return (training_data, testing_data)

if __name__ == '__main__':
    main()