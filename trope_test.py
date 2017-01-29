# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import imdb

# DATA FILES
TROPES_DATA = 'data/trope.csv'
WORKS_DATA = 'data/tvt_work.csv'
CAT_DATA = 'data/tvt_category.csv'

WORK_TROPE_LINKS_DATA = 'data/tvt_work_trope_link.csv'
WORK_CAT_LINKS_DATA = 'tvt_work_category_link.csv'
TROPE_CAT_LINKS_DATA = 'tvt_trope_category_link.csv'
CAT_LINKS_DATA = 'tvt_category_category_link.csv'
WIKI_WORK_LINKS_DATA = 'wiki_tvt_work_link.csv'
WIKI_WORK_DATA = 'wiki_work.csv'


def extract_imdb_ids(title_list):
    id_list = []
    for title in title_list[:100]:
        ia = imdb.IMDb()
        results = ia.search_movie(title)
        if results[0]:
            id_list.append(results[0].movieID)
        else:
            id_list.append(0)

    return id_list



if __name__ == "__main__":

    links_df = pd.read_csv(WORK_TROPE_LINKS_DATA, error_bad_lines=False)

    trope_df = pd.read_csv(TROPES_DATA, error_bad_lines=False)

    work_df = pd.read_csv(WORKS_DATA, error_bad_lines=False)

    #filter out works of literature
    film_works_df = work_df.loc[work_df['type'] == 'film']

    # Merge trope link data with valid film ids
    new_df = pd.merge(left=film_works_df,right=links_df, how='left', left_on='tvt_id', right_on='work_tvt_id')

    final_df = pd.merge(left=new_df,right=trope_df, how='left', left_on='trope_tvt_id', right_on='tvt_id')

    # Filters final data down to a single column: the movie title
    trope_counts_by_film_df = final_df.filter(items=['title_x'])

    # Counts the number of unique values in a column - in this case the titles of movies appearing for each trope
    trope_counts_by_film_df = trope_counts_by_film_df['title_x'].value_counts()

    #trope_counts_by_film_df = pd.DataFrame([trope_counts_by_film_df], columns = ["title", "trope_count"])

    #Outputs the movie title counts to a csv file
    trope_counts_by_film_df.to_csv('results/trope_frequency_by_film.csv', sep=',', encoding='utf-8')

    #Counts the trope frequency
    trope_frequency_series = final_df.filter(items=['title_y'])
    print type(trope_frequency_series)


    trope_frequency_series = trope_frequency_series['title_y'].value_counts()

    print type(trope_frequency_series)

    trope_frequency_df = trope_frequency_series.to_frame()
    trope_frequency_df.reset_index(level=0, inplace=True)
    trope_frequency_df.columns = ['trope', 'trope_count']


    print type(trope_frequency_df)
    print trope_frequency_df

    #trope_frequency_df.to_csv('results/trope_frequency.csv', sep=',', encoding='utf-8', header=['trope','trope_count'])

    # Prepare a Frequency Histogram
    '''tropeList = trope_frequency_df['trope'].tolist()
    trope_frequencyList = trope_frequency_df['trope_count'].tolist()
    tropeList = [line.strip() for line in tropeList]
    tropeList = [line.decode('utf-8').strip() for line in tropeList]

    pos = np.arange(len(tropeList))


    width = 5.0
    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(tropeList)
    plt.bar(pos, trope_frequencyList, width, color='r')
    plt.show()'''
    title_list = film_works_df.filter(items=['title'])['title'].tolist()

    #print title_list

    id_list = extract_imdb_ids(title_list)
    print id_list

    first_100_imdb_ids = ['0078748', '0107048', '0371724', '0758745', '0095016', '0118571', '0098663', '0058182', '0371746', '2771200', '0093010', '0096895', '0056217', '0478087', '0120483', '0018455', '0094862', '0120591', '0081777', '0083630', '0013442', '1502712', '0118276', '0112641', '0104868', '0047673', '0017925', '0163438', '0120903', '2404435', '0082348', '0172495', '0831887', '0053337', '0092086', '0442933', '0215750', '0133952', '0409459', '0346900', '0384537', '0370032', '0106582', '0070723', '0071402', '0465602', '0082031', '0119174', '0185183', '1068680', '0335266', '2096673', '0446059', '0074860', '0116695', '0059245', '0355295', '0122690', '3006802', '0408306', '2229511', '0090305', '0111301', '0116126', '0418279', '0095953', '0112642', '0119282', '0119528', '0050083', '5497458', '0421239', '0445934', '0098948', '0224397', '0099817', '0118884', '0340855', '3569230', '0204946', '0080752', '0183649', '0113855', '0328107', '0089092', '0382628', '1291150', '0100449', '1156398', '0952640', '0173886', '0230600', '0026174', '0335438', '0396269', '0472033', '1182345', '0033028', '0157503', '0449467']

    '''
    new_df = pd.merge(left=links_df,right=trope_df, how='left', left_on='trope_tvt_id', right_on='tvt_id')

    final_df = pd.merge(left=new_df,right=work_df, how='left', left_on='work_tvt_id', right_on='tvt_id')
    #df2 = pd.read_csv('data/')

    #df['work_tvt_id'].value_counts().plot(kind='bar')

    #plt.show()

    #print df.groupby('work_tvt_id').count()


    #print df['work_tvt_id'].value_counts()

    #filtered_df = df[(df['work_tvt_id'] > 200)]

    final_df.to_csv('results/test_results.csv', sep=',', encoding='utf-8')'''
