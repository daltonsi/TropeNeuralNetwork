import numpy as np
import pandas as pd
import time


'''
TRAINING DATA PREPERATION

DESCRIPTION: This script offers functions for manipulating a master data csv file
into a subsetted training csv data file for supervised machine learning models.

Every output of this script requires a series of columns that will serve as the
input columns for the neural network and column that will serve as the output
- target - column that the supervised machine learning model can train the input data against.

For example, the initial implementation of this script takes a subset set of trope_list
columns for a given movie as the input columns against the IMDB rating as the ouput column

Alternative implementations of this script may select a different arrangement of input columns
(e.g. different trope selections, movie genre, actors/actresses, director, year of release) and/or
a different selection for the ouput - target -  column (e.g. rotten tomatoes rating, meta-crtitic rating,
Box-office sucess, etc.)

INPUT: A MASTER CSV FILE containing all possible data columns that could be used for neural network training data
OUTPUT: A NEURAL NETWORK CSV FILE that will serve as training data in a supervised machine learning model creation script.

'''

# LOCATE MASTER FILE
MASTER_MOVIE_FILE = 'carton_trope_data/analysis/results/master_movie_data.csv'

# PREPARE COLUMN INCLUSION LIST
pos_trope_inclusion_list = ['763','2460','846','1611','11742','2964','13286','5019','17117','4336',\
	'4668','748','23318','19278','3137','7582','3372','51592','8703','13146','20669','21823','3461','7931','2455']

neg_trope_inclusion_list = ['261187','8364','3297','16351','3176','16953','15114','8568','1427','16455', \
	'308861','6142','4323','545','4511','8778','1617','10646','4702','22131','13542','577','9292','6313','1905']

final_trope_inclusion_list = pos_trope_inclusion_list + neg_trope_inclusion_list + ["imdb_rating"]

# LOAD THE MASTER FILE INTO PANDAS DATAFRAME
def load_master_file(master_data_file):
	master_df = pd.read_csv(master_data_file, error_bad_lines=False, encoding='latin-1',dtype={"imdb_rating": object})
	master_df['imdb_rating'] = pd.to_numeric(master_df['imdb_rating'], errors='coerce')
	return master_df

# FILTER DATAFRAME BY COLUMN INCLUSION LIST
def filter_master_dataframe(master_df,column_inclusion_list):
	training_df = master_df.filter(items=column_inclusion_list)
	return training_df

# CREATES THE TRAINING DATAFRAME
def create_training_dataframe():
	master_df = load_master_file(MASTER_MOVIE_FILE)
	filtered_master_df = filter_master_dataframe(master_df,final_trope_inclusion_list)
	filtered_master_df = filtered_master_df[np.isfinite(filtered_master_df['imdb_rating'])]
	return filtered_master_df

# OUTPUTS THE TRAINING DATAFRAME TO A CSV FILE
def pandas_to_csv(output_path,header,dataframe):
    try:
        dataframe.to_csv(output_path, sep=',', encoding='latin-1',header=header)
    except:
        print "Failure to create CSV file"

if __name__ == "__main__":
	training_df = create_training_dataframe()
	pandas_to_csv('training_data.csv',final_trope_inclusion_list,filtered_master_df)
