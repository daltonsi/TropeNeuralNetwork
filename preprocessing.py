# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv, time, sys, ast, operator
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

def calcTableFields(work_trope_links, tropeID_column='trope_tvt_id', movieID_column='work_tvt_id', count_threshold=25):
    '''Compiles MovieIDs and TropeIDs for data table rows and columns respectively'''
    print "Calculating table fields..."

    # Intialize data structures
    dataframe = pd.read_csv(work_trope_links, error_bad_lines=False, encoding='latin-1')
    tropeCounter = Counter()
    movieIDs = []
    tropeTrackerDict = {}

    # Count tropeIDs
    for index, row in dataframe[tropeID_column].iteritems():
        tropeCounter[row] += 1

    # Collect Movie IDs
    for index, row in dataframe[movieID_column].iteritems():
        movieIDs.append(row)
    movieIDs = set(movieIDs)

    # Collect tropes per movie
    tropeTrackerDict = {k: [] for k in movieIDs}


    # Filter tropes by count_threshold frequency or more
    tropeCounter = {k:v for k,v in tropeCounter.iteritems() if v > count_threshold}

    for row in zip(dataframe[movieID_column], dataframe[tropeID_column]):
        tropeTrackerDict[row[0]].append(row[1])
    tropeCounter = sorted(tropeCounter.items(), key=operator.itemgetter(1), reverse=True)

    print "Table fields complete!" + "\n"
    return tropeCounter, movieIDs, tropeTrackerDict


def generateTable(tropeCounter, movieIDs, tropeTrackerDict, count_threshold=25):
    '''Populates a pandas dataframe with trope occurances(column) for each movie(row)'''
    print "Generating the table..."
    #calculate table dimensions
    columns = [x[0] for x in tropeCounter]
    index = movieIDs

    # Create and fill blank dataframe
    df_ = pd.DataFrame(index=index, columns=columns)
    df_ = df_.fillna(0)

    # Use trope tracker information to fill table
    counter = 0
    for index, row in df_.iterrows():
        for trope in tropeTrackerDict[index]:
            try:
                if trope in columns:
                    df_.set_value(index,trope,1)
                else:
                    pass
            except:
                raise
        counter +=1
        print str(counter) + " of " + str(len(df_)) + " Keys Complete."

    df_['tvt_id'] = df_.index
    print "Table Complete!" + "\n"
    return df_


def json_to_pandas(json_file):
    ''' Loads json file into pandas dataframe'''
    data = pd.read_json(json_file)
    return data

def fix_imdb_data(imdb_df):
    '''Completes incomplete IMDB IDs'''
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 7, 'imdb_id'] = 'tt' + imdb_df['imdb_id']
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 6, 'imdb_id'] = 'tt0' + imdb_df['imdb_id']
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 5, 'imdb_id'] = 'tt00' + imdb_df['imdb_id']
    imdb_df.loc[imdb_df['imdb_id'].str.len() == 4, 'imdb_id'] = 'tt000' + imdb_df['imdb_id']
    return imdb_df

def create_imdb_dataframe():
    '''Creates a dataframe of IMDB data'''
    imdb_df = json_to_pandas(OMDB_DATA)
    imdb_df = imdb_df.filter(items=[u'actors', u'awards', u'country', u'director',u'genre', u'imdb_id', u'imdb_rating', u'imdb_votes', u'language', u'metascore', u'plot', u'rated', u'released', u'runtime', u'title', u'type', u'writer', u'year'])
    imdb_df = imdb_df.dropna(how='all')
    imdb_df = imdb_df.loc[imdb_df['type'].isin(['movie'])]
    #imdb_df[imdb_df['imdb_rating'].apply(lambda x: str(x).isdigit())]

    imdb_df['runtime'] = imdb_df['runtime'].str.replace(' min','').replace('N/A',np.NaN)
    return imdb_df

def combine_movie_trope_data(trope_df,imdb_df):
    ''' Combines trope and imdb data into one master dataframe'''
    rating_df = imdb_df.filter(items=[u'imdb_id',u'imdb_rating'])
    final_df = pd.merge(left=imdb_df, right=trope_df, how='left', left_on='imdb_id', right_on='imdb_id')
    del final_df['imdb_id']
    del final_df['tvt_id']
    del final_df['type']
    return final_df

def create_train_test(raw_dataframe):
    '''SPLITS RAW TRAINING DATA INTO TRAINING AND PERSONAL TEST DATA'''
    train_df, test_df = train_test_split(raw_dataframe, test_size = 0.2)
    return train_df, test_df

def filter_master_table(dataframe):
    '''Removes fields not to be used in the training and test data'''
    for field in ['actors','awards','country','director','genre','imdb_votes','language','metascore','plot','rated','released','runtime','title','writer','year']:
        del dataframe[field]
    return dataframe

if __name__ == "__main__":

    tropeCounter, movieIDs, tropeTrackerDict = calcTableFields(WORK_TROPE_LINKS_DATA)
    trope_df_ = generateTable(tropeCounter, movieIDs, tropeTrackerDict)
    movie_df = pd.read_csv(IMDB_ID_DATA, error_bad_lines=False, encoding='latin-1')
    movie_df = movie_df.filter(items=['imdb_id', 'tvt_id'])
    trope_df = pd.merge(left=movie_df, right=trope_df_, how='left', left_on='tvt_id', right_on='tvt_id')
    trope_df = fix_imdb_data(trope_df)
    imdb_df = create_imdb_dataframe()
    master_df = combine_movie_trope_data(trope_df, imdb_df)
    master_df = filter_master_table(master_df)
    print len(master_df)
    master_df[['imdb_rating']] = master_df[['imdb_rating']].apply(pd.to_numeric, errors='coerce')
    master_df = master_df[np.isfinite(master_df['imdb_rating'])]
    print len(master_df)

    train, test = create_train_test(master_df)
    train.to_csv('results/training.csv', sep=',', encoding='latin-1', index=False, header=False)
    test.to_csv('results/test.csv', sep=',', encoding='latin-1', index=False, header=False)
