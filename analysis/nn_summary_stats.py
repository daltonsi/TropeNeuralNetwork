# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import time
import sys
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import operator
import training_data_prep as tdp


MASTER_TROPE = 'results/master_trope.csv'
TRAIN = 'results/train_trope.csv'
MASTER = 'results/master.csv'

'''
FIND CORRELATIONS BETWEEN DATA COLUMNS
'''

# LOAD THE MASTER CSV FILE INTO PANDAS DATAFRAME
def load_master_file(master_data_file):
	master_df = pd.read_csv(master_data_file, error_bad_lines=False, encoding='latin-1',header=0)
	return master_df


#Calculates the pearson coefficient between the target_column and each of the input columns
#  data_file = a pandas dataframe (pandas df)
#  target_column = the column name of the dependent variables (string)
#  input_columns =  the columns names the of the independent variables (list of strings)
def calc_correlations(dataframe, target_column, input_columns, output_path=None):

    correlations = {}
    index = 0
    for column in dataframe.columns:
        try:
            trimmed_df = dataframe.filter(items=[target_column, column])
            trimmed_df = trimmed_df[np.isfinite(trimmed_df[target_column])]
            trimmed_df = trimmed_df[np.isfinite(trimmed_df[column])]
            trimmed_df.apply(lambda x: pd.to_numeric(x))#, errors='ignore'))
            correlations[column] = pearsonr(trimmed_df[target_column],trimmed_df[column])
        except:
            print "Error calculating correaltion"
            pass


        index +=1
    if output_path:
        with open(output_path, 'wb') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Variable", "pearson", "p-value"])
            for key, value in correlations.items():
                writer.writerow([key, value[0],value[1]])
    return correlations



if __name__ == "__main__":
    dataframe = load_master_file(MASTER)
    calc_correlations(dataframe, 'imdb_rating', dataframe.columns, 'master_master_correlations.csv')
