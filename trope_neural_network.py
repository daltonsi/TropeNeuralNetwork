# Code borrowed from http://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import time

MASTER_MOVIE_FILE = 'carton_trope_data/analysis/results/master_movie_data.csv'

pos_trope_inclusion_list = ['763','2460','846','1611','11742','2964','13286','5019','17117','4336',\
	'4668','748','23318','19278','3137','7582','3372','51592','8703','13146','20669','21823','3461','7931','2455']

neg_trope_inclusion_list = ['261187','8364','3297','16351','3176','16953','15114','8568','1427','16455', \
	'308861','6142','4323','545','4511','8778','1617','10646','4702','22131','13542','577','9292','6313','1905']

final_trope_inclusion_list = pos_trope_inclusion_list + neg_trope_inclusion_list + ["imdb_rating"]

def load_master_file(master_data_file):
	master_df = pd.read_csv(master_data_file, error_bad_lines=False, encoding='latin-1',dtype={"imdb_rating": object})
	master_df['imdb_rating'] = pd.to_numeric(master_df['imdb_rating'], errors='coerce')
	return master_df

def filter_master_dataframe(master_df,list_of_headings):
	neural_network_df = master_df.filter(items=list_of_headings)
	return neural_network_df

def create_nn_dataframe():
	master_df = load_master_file(MASTER_MOVIE_FILE)
	filtered_master_df = filter_master_dataframe(master_df,final_trope_inclusion_list)
	filtered_master_df = filtered_master_df[np.isfinite(filtered_master_df['imdb_rating'])]
	return filtered_master_df

def pandas_to_csv(output_path,header,dataframe):
    try:
        dataframe.to_csv(output_path, sep=',', encoding='latin-1',header=header)
    except:
        print "Failure to create CSV file"

# load dataset
def create_neural_network(input_data):

	dataframe = pd.read_csv(input_data, delim_whitespace=False, header=0)
	dataset = dataframe.values
	# split into input (X) and output (Y) variables
	X = dataset[:,0:50]
	Y = dataset[:,50]
	print Y
	print time.clock()

	# define base mode
	# Guide to Sequential Model: https://keras.io/getting-started/sequential-model-guide/

	# Sequential model constructer takes a list of layer instances
	#   these layers can be specified ina direct constructor OR sequentially with an "add" method
	#   the instance layer should specifiy the dimensions of the input shape add(Dense(32, input_shape=(784,)))
	#

	def baseline_model():
		# create model
		model = Sequential()

	    # Dense('size_of_output')
		model.add(Dense(50, input_dim=50, init='normal', activation='relu'))
		model.add(Dense(1, init='normal'))
		# Compile model
		model.compile(loss='mean_squared_error', optimizer='adam')
		return model


	# fix random seed for reproducibility
	seed = 7
	np.random.seed(seed)
	# evaluate model with standardized dataset
	estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=100, batch_size=5, verbose=0)


	kfold = KFold(n_splits=10, random_state=seed)
	results = cross_val_score(estimator, X, Y, cv=kfold)
	print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
	print time.clock()

if __name__ == "__main__":
	#filtered_master_df = create_nn_dataframe()
	#pandas_to_csv('nn_data.csv',final_trope_inclusion_list,filtered_master_df)
	create_neural_network('nn_data.csv')
