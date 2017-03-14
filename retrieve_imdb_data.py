import pandas as pd
import numpy as np
import omdb
import json


'''
RETRIEVE IMDB DATA

This script prepares a list of movie IMDB ids that are called through the OMDB appearing
to retrieve a data profile for each movie in the form of a json response.

INPUT: CSV Data file containing of column of IMDB ids.
OUTPUT: JSON file containing list of movie profiles
'''

# LOCATE FILE WITH IMDB ID COLUMN
IMDB_ID_DATA = 'dd_data/imdb_id_master.csv'

time.clock()

# MODIFIES INCOMPLETE IMDB IDS
def fix_imdb_data(IMDB_ID_DATA):
    list_of_imdb_ids = IMDB_ID_DATA['imdb_id'].values.tolist()
    for imdb_id in range(0,len(list_of_imdb_ids)):
        if len(list_of_imdb_ids[imdb_id]) == 7:
            list_of_imdb_ids[imdb_id] = 'tt' + list_of_imdb_ids[imdb_id]
        elif len(list_of_imdb_ids[imdb_id]) == 6:
            list_of_imdb_ids[imdb_id] = 'tt0' + list_of_imdb_ids[imdb_id]
        elif len(list_of_imdb_ids[imdb_id]) == 5:
            list_of_imdb_ids[imdb_id] = 'tt00' + list_of_imdb_ids[imdb_id]
        elif len(list_of_imdb_ids[imdb_id]) == 4:
            list_of_imdb_ids[imdb_id] = 'tt000' + list_of_imdb_ids[imdb_id]
        else:
            pass
    return list_of_imdb_ids

# ITERATES THROUGH LIST OF IMDB IDS TO RETRIEVE MOVIE PROFILES
def get_imdb_json(list_of_imdb_ids):
    counter = 0
    json_list = []
    for imdb_id in list_of_imdb_ids:
        print imdb_id
        print counter + 1
        try:
            new_json = omdb.imdbid(imdb_id)
        except:
            new_json = 0
        print new_json
        json_list.append(new_json)
        counter +=1
    return json_list

if __name__ == "__main__":

    imdb_id_data_df = pd.read_csv(IMDB_ID_DATA, error_bad_lines=False)
    revised = fix_imdb_data(imdb_id_data_df)
    final = get_imdb_json(revised)

    with open('imdb_data.txt', 'w') as outfile:
        json.dump(final, outfile)
