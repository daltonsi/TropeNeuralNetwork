# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import time
import sys
import ast


# SAM DATA FILES
TROPES_DATA = 'data/trope.csv'
WORKS_DATA = 'data/tvt_work.csv'
CAT_DATA = 'data/tvt_category.csv'

WORK_TROPE_LINKS_DATA = 'data/tvt_work_trope_link.csv'
WORK_CAT_LINKS_DATA = 'tvt_work_category_link.csv'
TROPE_CAT_LINKS_DATA = 'tvt_trope_category_link.csv'
CAT_LINKS_DATA = 'tvt_category_category_link.csv'
WIKI_WORK_LINKS_DATA = 'wiki_tvt_work_link.csv'
WIKI_WORK_DATA = 'wiki_work.csv'


# DALTON DATA FILES
IMDB_ID_DATA = 'dd_data/imdb_id_master.csv'
MOVIE_TROPE_LISTS = 'dd_data/movie_tropes.csv'


time.clock()

def combine_movie_trope_data():
        movie_df = pd.read_csv(IMDB_ID_DATA, error_bad_lines=False, encoding='latin-1')
        movie_tropes_df = pd.read_csv(MOVIE_TROPE_LISTS, error_bad_lines=False, encoding='latin-1')
        new_df = pd.merge(left=movie_df, right=movie_tropes_df, how='left', left_on='tvt_id', right_on='tvt_id')
        return new_df

def pandas_to_csv(output_path,header,dataframe):
    try:
        dataframe.to_csv(output_path, sep=',', encoding='latin-1',header=header)
    except:
        print "Failure to create CSV file"

def create_default_trope_columns(dataframe):
    try:
        trope_work_link_df = pd.read_csv(WORK_TROPE_LINKS_DATA, error_bad_lines=False, encoding='latin-1')

        trope_list = set(trope_work_link_df['trope_tvt_id'].tolist())
    except:
        print "Error creating trope list:", sys.exc_info()[0]
        raise
    try:
        for trope in trope_list:
            dataframe[trope] = 0
        print dataframe
    except:
        print "Error creating default trope columns:", sys.exc_info()[0]
        raise
    try:
        for index, row in dataframe.iterrows():
            print row
            x = row[4]
            x = ast.literal_eval(x)
            relevant_tropes = [n for n in x]
            for trope in relevant_tropes:
                print trope
                #dataframe.set_value(row, row[trope], 1)
                dataframe.iloc[index, dataframe.columns.get_loc(trope)] = 1
    except:
        print "Error setting default trope values", sys.exc_info()[0]
        raise

    return dataframe, trope_list


if __name__ == "__main__":
    new_df = combine_movie_trope_data()
    final_dataframe, trope_list = create_default_trope_columns(new_df)
    print final_dataframe
    header = ['tvt_id','title','imdb_id','imdb_rating','trope_list'] + list(trope_list)
    pandas_to_csv('results/master_movie_data.csv',header,final_dataframe)

    # This
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][167])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][464])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][475])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][511])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][763])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][777])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1048])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1081])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1085])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1251])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1427])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1605])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1611])
    print "Alien Trope Test: " + str(final_dataframe.iloc[0][1779])

    print "Alien FAIL Trope Test: " + str(final_dataframe.iloc[0][548])
    print "Alien FAIL Trope Test: " + str(final_dataframe.iloc[0][325])
