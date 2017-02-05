# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

#Make connection to raw data files
TROPES_DATA = 'data/trope.csv'
CAT_DATA = 'data/tvt_category.csv'
TROPE_CAT_LINKS_DATA = 'data/tvt_trope_category_link.csv'
CAT_LINKS_DATA = 'data/tvt_category_category_link.csv'

#df = pd.read_csv(open('out.dbtropes-feature.tsv'), sep='\s+', header=0, names=['a','b'])

# Load data table into pandas data frame
tropes_df = pd.read_csv(open(TROPES_DATA),encoding='latin-1')
cat_df = pd.read_csv(open(CAT_DATA),encoding='latin-1')

df = pd.read_csv(open(TROPE_CAT_LINKS_DATA))#, header=0, names=['link_id','child_tvt_id','parent_tvt_id'])
#df = pd.read_csv(open(TROPE_CAT_LINKS_DATA))#, header=0, names=['link_id','child_tvt_id','parent_tvt_id'])
merged_df = pd.merge(left=df,right=tropes_df, how='left', left_on='trope_tvt_id', right_on='tvt_id')
final_df = pd.merge(left=merged_df,right=cat_df, how='left', left_on='category_tvt_id', right_on='tvt_id')

final_df =  final_df.filter(items=['trope_tvt_id','category_tvt_id','title_x','title_y'])

print final_df

# Create edge pairs for network processing
nx_edge_pairs = [(x[3],x[2]) for x in final_df.to_records(index=False)]

# Create graph object
g = nx.MultiDiGraph()

# Add edges from tuple pairs extracted from data_frame
g.add_edges_from(nx_edge_pairs)

print len(g.nodes())
# identify edges that have less that have a degree centrality of less than 3
remove = [node for node,degree in g.degree().items() if degree < 175]

# remove unwanted nodes from the graph
g.remove_nodes_from(remove)
print len(g.nodes())



d = nx.degree(g)

pos = nx.spring_layout(g,scale=1) #default to scale=1
nx.draw(g,with_labels=True, node_size=[v * 100 for v in d.values()],font_color='blue')
plt.show()
#plt.savefig('cat_links_six_plus.png')
#plt.savefig('cat_links_six_plus.png')
