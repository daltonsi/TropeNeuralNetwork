# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import time
import sys
import ast

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

def create_trope_dataframe():
    movie_df = pd.read_csv(IMDB_ID_DATA, error_bad_lines=False, encoding='latin-1')
    movie_df = fix_imdb_data(movie_df)
    movie_tropes_df = pd.read_csv(MOVIE_TROPE_LISTS, error_bad_lines=False, encoding='latin-1')
    new_df = pd.merge(left=movie_df, right=movie_tropes_df, how='left', left_on='tvt_id', right_on='tvt_id')
    trope_df = new_df.filter(items=['imdb_id', 'trope_list'])
    try:
        trope_work_link_df = pd.read_csv(WORK_TROPE_LINKS_DATA, error_bad_lines=False, encoding='latin-1')

        trope_list = set(trope_work_link_df['trope_tvt_id'].tolist())
    except:
        print "Error creating trope list:", sys.exc_info()[0]
        raise
    try:
        for trope in trope_list:
            trope_df[trope] = 0
        print trope_df
    except:
        print "Error creating default trope columns:", sys.exc_info()[0]
        raise
    try:
        for index, row in trope_df.iterrows():
            print row
            x = row[1]
            x = ast.literal_eval(x)
            relevant_tropes = [n for n in x]
            for trope in relevant_tropes:
                print trope
                #dataframe.set_value(row, row[trope], 1)
                trope_df.iloc[index, trope_df.columns.get_loc(trope)] = 1
    except:
        print "Error setting default trope values", sys.exc_info()[0]
        raise
    return trope_df.drop('trope_list', 1)

def create_imdb_dataframe():
    imdb_df = json_to_pandas(OMDB_DATA)
    imdb_df = imdb_df.filter(items=[u'actors', u'awards', u'country', u'director',u'genre', u'imdb_id', u'imdb_rating', u'imdb_votes', u'language', u'metascore', u'plot', u'rated', u'released', u'runtime', u'title', u'type', u'writer', u'year'])
    imdb_df = imdb_df.dropna(how='all')
    imdb_df = imdb_df.loc[imdb_df['type'].isin(['movie'])]
    imdb_df['runtime'] = imdb_df['runtime'].str.replace(' min','').replace('N/A',np.NaN)
    return imdb_df

def combine_movie_trope_data():
    trope_df = create_trope_dataframe()
    imdb_df = create_imdb_dataframe()
    final_df = pd.merge(left=imdb_df, right=trope_df, how='left', left_on='imdb_id', right_on='imdb_id')
    return final_df


if __name__ == "__main__":
    print "Program Starting at " + str(time.clock())
    new_df = combine_movie_trope_data()
    new_df.to_csv('results/master_movie_data.csv', sep=',', encoding='latin-1')

    # This
    print "Alien Trope Test: " + str(new_df.iloc[0][167])
    print "Alien Trope Test: " + str(new_df.iloc[0][464])
    print "Alien Trope Test: " + str(new_df.iloc[0][475])
    print "Alien Trope Test: " + str(new_df.iloc[0][511])
    print "Alien Trope Test: " + str(new_df.iloc[0][763])
    print "Alien Trope Test: " + str(new_df.iloc[0][777])
    print "Alien Trope Test: " + str(new_df.iloc[0][1048])
    print "Alien Trope Test: " + str(new_df.iloc[0][1081])
    print "Alien Trope Test: " + str(new_df.iloc[0][1085])
    print "Alien Trope Test: " + str(new_df.iloc[0][1251])
    print "Alien Trope Test: " + str(new_df.iloc[0][1427])
    print "Alien Trope Test: " + str(new_df.iloc[0][1605])
    print "Alien Trope Test: " + str(new_df.iloc[0][1611])
    print "Alien Trope Test: " + str(new_df.iloc[0][1779])

    print "Alien FAIL Trope Test: " + str(new_df.iloc[0][548])
    print "Alien FAIL Trope Test: " + str(new_df.iloc[0][325])
