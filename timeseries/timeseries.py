import sqlite3 as sqlite
import csv

# wikipedia data
infile = open('wiki_work.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_wiki = []
for row in reader:
	lot_wiki.append((row.get('wiki_id'),row.get('type'),row.get('year')))
infile.close()

# links between wikipedia and tvtropes pages
infile = open('wiki_tvt_work_link.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_link = []
for row in reader:
		lot_link.append((row.get('wiki_id'),row.get('tvt_id')))
infile.close()

# tvtropes data
infile = open('tvt_work.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_tvt = []
for row in reader:
	lot_tvt.append((row.get('tvt_id'),row.get('title').decode('utf-8')))
infile.close()

# tropes data
infile = open('tvt_work_trope_link.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_tropes = []
for row in reader:
	lot_tropes.append((row.get('work_tvt_id'),row.get('trope_tvt_id')))
infile.close()

con = sqlite.connect('tvt_timeseries.db')
cur = con.cursor()

# create tables
cur.execute("DROP TABLE IF EXISTS wiki")
cur.execute("DROP TABLE IF EXISTS tvt")
cur.execute("DROP TABLE IF EXISTS link")
cur.execute("DROP TABLE IF EXISTS tropes")
cur.execute("CREATE TABLE wiki (wiki_id int, type varchar(255), year int)")
cur.execute("CREATE TABLE tvt (tvt_id int, title varchar(255))")
cur.execute("CREATE TABLE link (wiki_id int, tvt_id int)")
cur.execute("CREATE TABLE tropes (tvt_id int, trope_id int)")

# insert data into tables
cur.executemany("INSERT INTO wiki VALUES (?,?,?)", lot_wiki)
con.commit()
cur.executemany("INSERT INTO tvt VALUES (?,?)", lot_tvt)
con.commit()
cur.executemany("INSERT INTO link VALUES (?,?)", lot_link)
con.commit()
cur.executemany("INSERT INTO tropes VALUES (?,?)", lot_tropes)
con.commit()

cur.execute("SELECT wiki.year, tvt.title, wiki.type, wiki.wiki_id, link.tvt_id, COUNT(*) FROM wiki INNER JOIN link ON wiki.wiki_id=link.wiki_id INNER JOIN tropes ON tropes.tvt_id=link.tvt_id INNER JOIN tvt ON link.tvt_id=tvt.tvt_id WHERE wiki.type='film' GROUP BY tropes.tvt_id ORDER BY wiki.year")
rows = cur.fetchall()
outfile = open('tvt_timeseries.csv','w')
writer = csv.DictWriter(outfile,delimiter=',',fieldnames=['year','title','type','wiki_id','tvt_id','trope_count'])
writer.writeheader()
# Print statement is for error checking purposes, feel free to delete print statements
for row in rows:
	print 'Year: %s | Title: %s | Type: %s | Wiki ID: %s | TVT ID: %s | Tropes: %s' % (row[0],row[1],row[2],row[3],row[4],row[5])
	# NOTE: nonstandard characters (such as ä) are dropped from titles during ascii encode process
	writer.writerow({'year':row[0],'title':row[1].encode('ascii','ignore'),'type':row[2],'wiki_id':row[3],'tvt_id':row[4],'trope_count':row[5]})
outfile.close()
