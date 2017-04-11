# Code borrowed from http://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.callbacks import ModelCheckpoint
from keras.wrappers.scikit_learn import KerasRegressor
from keras.optimizers import SGD, RMSprop
from keras.models import load_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import time
from collections import Counter
import csv

'''
CREATES INPUT AND OUTPUT VECTORS, TRAINS A NEURAL NETWORK
'''


TRAIN = pd.read_csv('results/training.csv', sep=',', header=None,  encoding='utf-8')
TEST = pd.read_csv('results/test.csv', sep=',', header=None,  encoding='utf-8')
'''
TRAIN THE NEURAL NETWORK
'''

seed = 7
np.random.seed(seed)

def results_to_csv(filename, results):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Category"])
        index = 0
        for val in results:
            writer.writerow([index, float(val)])
            index +=1

def create_neural_network(training, test, trainNewModel = False, modelFilename = 'test.h5'):
     ''' TRAINS A NEURAL NETWORK AND OUPUTS A PREDICTION OF RESULTS ON TEST DATA'''
     dataset = training.values
	 # split into input (X) and output (Y) variables
     input_dimension = len(dataset[0])-1
     X = training.iloc[:,1:].values
     Y = training.iloc[:,0:1].values

     # split test data into input and output variables
     TEST_DATA = test.values
     TEST_X = test.iloc[:,1:]
     TEST_Y = test.iloc[:,:1]

     def baseline_model():
        # create model
          model = Sequential()

	    # Dense('size_of_output')
          model.add(Dense(input_dimension, input_dim=input_dimension, init='normal', activation='relu'))
		#model.add(Dense(6, init='normal', activation='relu'))
          model.add(Dense(1, init='normal'))
          print
		# Compile model
          model.compile(loss='mean_squared_error', optimizer='adam')
          if trainNewModel == True:
              history = model.fit(X,Y,nb_epoch=100,batch_size=50)
              #model.save_weights("model_v1.h5")
          model.load_weights("model_v1.h5")
          predictions = model.predict(np.array(TEST_X))
          predictions = pd.Series([float(x[0]) for x in predictions])
          #results_to_csv('results_1.csv', predictions)
          return model, predictions

     model, predictions = baseline_model()


     results_df = pd.concat([predictions, TEST_Y], axis=1)
     print results_df
     results_df.columns = ['prediction', 'label']
     results_df['diff'] = abs(results_df['prediction'] - results_df['label'])**2
     print results_df
     print results_df["diff"].mean()

	# OPTIONAL: Evaluate using K-Folds
	# evaluate model with standardized dataset
     #estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=100, batch_size=5, verbose=1)


     #kfold = KFold(n_splits=10, random_state=seed)
     #results = cross_val_score(estimator, X, Y, cv=kfold)
     #print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
     #print time.clock()

if __name__ == "__main__":
    try:
        create_neural_network(TRAIN, TEST)
    except:
        raise
