# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite

TROPES_DATA = 'data/trope.csv'
WORKS_DATA = 'data/tvt_work.csv'

WORK_TROPE_LINKS_DATA = 'data/tvt_work_trope_link.csv'


tropes_df = pd.read_csv(open(TROPES_DATA),encoding='latin-1')
works_df = pd.read_csv(open(WORKS_DATA),encoding='latin-1')
work_trope_df = pd.read_csv(open(WORK_TROPE_LINKS_DATA),encoding='latin-1')

merged_df = pd.merge(left=work_trope_df,right=works_df, how='left', left_on='work_tvt_id', right_on='tvt_id')
final_df = pd.merge(left=merged_df,right=tropes_df, how='left', left_on='trope_tvt_id', right_on='tvt_id')

final_df =  final_df.filter(items=['title_x','title_y'])

print final_df

tropes = final_df["title_y"].tolist()[:91]
works = final_df["title_x"].tolist()[:91]

#works = [str(x)+'a' for x in works]
#tropes = [str(x)+'b' for x in tropes]


work_trope_links = zip(works,tropes)

B = nx.Graph()
B.add_nodes_from(tropes, bipartite=0)
B.add_nodes_from(works, bipartite=1)
B.add_edges_from(work_trope_links)


print nx.is_connected(B)

X, Y = bipartite.sets(B)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
nx.draw(B, pos=pos, with_labels=True)
plt.show()
