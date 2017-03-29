# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import time
import sys
import ast
from sklearn.model_selection import train_test_split
from collections import Counter

'''
CREATE MASTER TABLE

DESCRIPTION: This files combines movie data from multiple data files into one master table.

ROWS: Movies
COLUMNS: Movie attributes

'''

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
OMDB_DATA = 'imdb_data.json'


time.clock()

# Helper function to combine_movie_trope_data
def json_to_pandas(json_file):
    data = pd.read_json(json_file)
    return data

def fix_imdb_data(imdb_df):
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 7, 'imdb_id'] = 'tt' + imdb_df['imdb_id']
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 6, 'imdb_id'] = 'tt0' + imdb_df['imdb_id']
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 5, 'imdb_id'] = 'tt00' + imdb_df['imdb_id']
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 4, 'imdb_id'] = 'tt000' + imdb_df['imdb_id']
    return imdb_df

# Creates a trope inclusion list based on a threshold occurance of a particular trope in the master data
def calc_trope_frequencies():
    movie_trope_links_df = pd.read_csv(WORK_TROPE_LINKS_DATA, error_bad_lines=False, encoding='latin-1')
    trope_counts = Counter()
    for row in movie_trope_links_df['trope_tvt_id']:
        trope_counts[row] += 1

    # SPECIFY THRESHOLD BELOW
    trope_inclusion_list = [trope for trope in trope_counts.keys() if trope_counts[trope] > 25]

    return trope_inclusion_list

def create_trope_dataframe(trope_inclusion_list):
    movie_df = pd.read_csv(IMDB_ID_DATA, error_bad_lines=False, encoding='latin-1')
    movie_df = fix_imdb_data(movie_df)
    movie_tropes_df = pd.read_csv(MOVIE_TROPE_LISTS, error_bad_lines=False, encoding='latin-1')
    new_df = pd.merge(left=movie_df, right=movie_tropes_df, how='left', left_on='tvt_id', right_on='tvt_id')
    trope_df = new_df.filter(items=['imdb_id', 'trope_list'])
    trope_df = trope_df.drop_duplicates(subset="imdb_id")
    #print trope_df
    try:
        trope_work_link_df = pd.read_csv(WORK_TROPE_LINKS_DATA, error_bad_lines=False, encoding='latin-1')

        trope_list = set(trope_work_link_df['trope_tvt_id'].tolist())
    except:
        print "Error creating trope list:", sys.exc_info()[0]
        raise
    try:
        for trope in trope_list:
            if trope in trope_inclusion_list:
                trope_df[trope] = 0
        #print trope_df
    except:
        print "Error creating default trope columns:", sys.exc_info()[0]
        raise
    try:
        for index, row in trope_df.iterrows():
            x = row[1]
            x = ast.literal_eval(x)
            relevant_tropes = [n for n in x if n in trope_inclusion_list]
            for trope in relevant_tropes:
                #print trope
                #dataframe.set_value(row, row[trope], 1)
                trope_df.iloc[index, trope_df.columns.get_loc(trope)] = 1
    except:
        print "Error setting default trope values", sys.exc_info()[0]
        pass
    return trope_df.drop('trope_list', 1)

def create_imdb_dataframe():
    imdb_df = json_to_pandas(OMDB_DATA)
    imdb_df = imdb_df.filter(items=[u'actors', u'awards', u'country', u'director',u'genre', u'imdb_id', u'imdb_rating', u'imdb_votes', u'language', u'metascore', u'plot', u'rated', u'released', u'runtime', u'title', u'type', u'writer', u'year'])
    imdb_df = imdb_df.dropna(how='all')
    imdb_df = imdb_df.loc[imdb_df['type'].isin(['movie'])]
    imdb_df['runtime'] = imdb_df['runtime'].str.replace(' min','').replace('N/A',np.NaN)
    return imdb_df

def combine_movie_trope_data(trope_inclusion_list):
    trope_df = create_trope_dataframe(trope_inclusion_list)
    #print trope_df
    imdb_df = create_imdb_dataframe()
    rating_df = imdb_df.filter(items=[u'imdb_id',u'imdb_rating'])
    final_df = pd.merge(left=imdb_df, right=trope_df, how='left', left_on='imdb_id', right_on='imdb_id')
    trope_df = pd.merge(left=rating_df, right=trope_df, how='left', left_on='imdb_id', right_on='imdb_id')
    del trope_df['imdb_id']
    return final_df, trope_df

def create_test_train_data(dataframe):
    train, test = train_test_split(dataframe, test_size = 0.2)
    #train_trope = train.drop(labels=[u'actors', u'awards', u'country', u'director',u'genre', u'imdb_id', u'imdb_votes', u'language', u'metascore', u'plot', u'rated', u'released', u'runtime', u'title', u'type', u'writer', u'year'])
    #test_trope = test.drop(labels=[u'actors', u'awards', u'country', u'director',u'genre', u'imdb_id', u'imdb_votes', u'language', u'metascore', u'plot', u'rated', u'released', u'runtime', u'title', u'type', u'writer', u'year'])
    return train, test, train_trope, test_trope

if __name__ == "__main__":
    trope_inclusion_list = calc_trope_frequencies()
    print "Program Starting at " + str(time.clock())
    master_df,trope_df = combine_movie_trope_data(trope_inclusion_list)
    train, test, train_trope, test_trope = create_test_train_data(master_df)
    #train_trope, test_trope = create_test_train_data(trope_df)
    master_df.to_csv('results/master.csv', sep=',', encoding='latin-1')
    train.to_csv('results/master_train.csv', sep=',', encoding='latin-1')
    test.to_csv('results/master_test.csv', sep=',', encoding='latin-1')
    #trope_df.to_csv('results/master_trope.csv', sep=',', encoding='latin-1')
    #train_trope.to_csv('results/train_trope.csv', sep=',', encoding='latin-1')
    #test_trope.to_csv('results/test_trope.csv', sep=',', encoding='latin-1')

    # This
    print "Alien Trope Test: " + str(master_df.iloc[0][167])
    print "Alien Trope Test: " + str(master_df.iloc[0][464])
    print "Alien Trope Test: " + str(master_df.iloc[0][475])
    print "Alien Trope Test: " + str(master_df.iloc[0][511])
    print "Alien Trope Test: " + str(master_df.iloc[0][763])
    print "Alien Trope Test: " + str(master_df.iloc[0][777])
    print "Alien Trope Test: " + str(master_df.iloc[0][1048])
    print "Alien Trope Test: " + str(master_df.iloc[0][1081])
    print "Alien Trope Test: " + str(master_df.iloc[0][1085])
    print "Alien Trope Test: " + str(master_df.iloc[0][1251])
    print "Alien Trope Test: " + str(master_df.iloc[0][1427])
    print "Alien Trope Test: " + str(master_df.iloc[0][1605])
    print "Alien Trope Test: " + str(master_df.iloc[0][1611])
    print "Alien Trope Test: " + str(master_df.iloc[0][1779])

    print "Alien FAIL Trope Test: " + str(master_df.iloc[0][548])
    print "Alien FAIL Trope Test: " + str(master_df.iloc[0][325])
