# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import time
import sys
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import operator


MASTER_MOVIE_FILE = 'results/master_movie_data.csv'

def load_master_file(MASTER_MOVIE_FILE):
    #master_df = pd.read_csv(MASTER_MOVIE_FILE, error_bad_lines=False, encoding='latin-1',usecols=['imdb_rating', '229377'],dtype={"imdb_rating": object})
    master_df = pd.read_csv(MASTER_MOVIE_FILE, error_bad_lines=False, encoding='latin-1',dtype={"imdb_rating": object})

    correlations = {}
    master_df['imdb_rating'] = pd.to_numeric(master_df['imdb_rating'], errors='coerce')
    master_df = master_df.drop(['tvt_id', 'title', 'imdb_id','trope_list'], axis=1)

    # Removes rows with na in imdb_rating column
    master_df = master_df[np.isfinite(master_df['imdb_rating'])]

    ratings_df = master_df.filter(items=['imdb_rating'])

    ratings_df.apply(lambda x: pd.to_numeric(x, errors='ignore'))

    trope_hits_df = ratings = master_df.drop(['imdb_rating'], axis=1)
    trope_hits_df.apply(lambda x: pd.to_numeric(x, errors='ignore'))

    cols = [col for col in trope_hits_df.columns]

    index = 0
    for column in trope_hits_df:
        try:
            correlations[cols[index]] = pearsonr(ratings_df['imdb_rating'],trope_hits_df[column])
        except:
            correlations[cols[index]] = "na"
        index +=1

    sorted_correlations = sorted(correlations.iteritems(), key=lambda x: x[1][0], reverse=True)
    print len(sorted_correlations)
    sorted_correlations = [(i[0],(float(i[1][0]),float(i[1][1]))) for i in sorted_correlations if not np.isnan(i[1][0])]
    print len(sorted_correlations)

    #print sorted_correlations
    #sorted_correlations = sorted_correlations[np.logical_not(np.isnan(sorted_correlations[1][0]))]
    #print len(sorted_correlations)
    #print type(sorted_correlations[0][1][0])
    bottom = sorted(sorted_correlations, key=lambda x: x[1][0], reverse=True)[-2500:]
    top = sorted(sorted_correlations, key=lambda x: x[1][0], reverse=True)[:2500]

    print bottom
    print top


    '''#sorted_correlations = sorted(correlations.items(), key=operator.itemgetter(0))
    #print correlations.values()
    fig = plt.figure()
    fig.suptitle('IMDB Rating vs. Dull Surprise Trope', fontsize=20)
    plt.scatter(master_df['1905'],master_df['imdb_rating'])
    plt.xlabel('Trope: Dull Surprise')
    plt.ylabel('IMDB Rating')


    slope_bit_sweet = -0.138
    # Draw these two points with big triangles to make it clear
    # where they lie
    plt.scatter([0, 1], [0, slope_bit_sweet], marker='^', s=150, c='r')
    plt.plot([0, 1], [0, slope_bit_sweet], c='r')

    fig.savefig('dullsurprise_v_imdbRating.jpg')'''



if __name__ == "__main__":

    load_master_file(MASTER_MOVIE_FILE)
