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
cur.execute("DROP TABLE IF EXISTS link")
cur.execute("DROP TABLE IF EXISTS tropes")
cur.execute("CREATE TABLE wiki (wiki_id int, type varchar(255), year int)")
cur.execute("CREATE TABLE link (wiki_id int, tvt_id int)")
cur.execute("CREATE TABLE tropes (tvt_id int, trope_id int)")

# insert data into tables
cur.executemany("INSERT INTO wiki VALUES (?,?,?)", lot_wiki)
con.commit()
cur.executemany("INSERT INTO link VALUES (?,?)", lot_link)
con.commit()
cur.executemany("INSERT INTO tropes VALUES (?,?)", lot_tropes)
con.commit()

# Replace tropes.trope_id with desired trope id from trope.csv (under tvt_id in that file)
cur.execute("SELECT wiki.year, COUNT(*) FROM wiki INNER JOIN link ON wiki.wiki_id=link.wiki_id INNER JOIN tropes ON tropes.tvt_id=link.tvt_id WHERE wiki.type='film' AND tropes.trope_id=3462 GROUP BY wiki.year ORDER BY wiki.year")
rows = cur.fetchall()
# Feel free to rename output file to match desired trope
outfile = open('tvt_jerkass_timeseries.csv','w')
writer = csv.DictWriter(outfile,delimiter=',',fieldnames=['year','num_films'])
writer.writeheader()
# Print statement is for error checking purposes, feel free to delete print statements
print 'Jerkass Occurrences by Year:'
for row in rows:
	print 'Year: %s | Number of Films: %s' % (row[0],row[1])
	writer.writerow({'year':row[0],'num_films':row[1]})
outfile.close()
