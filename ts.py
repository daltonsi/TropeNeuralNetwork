import sqlite3 as sqlite
import csv
from sklearn import linear_model
import numpy as np

# IMDB movie data
infile = open('master_train.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_movie = []
for row in reader:
	imdb_id = row.get('imdb_id')[2:len(row.get('imdb_id'))]
	lot_movie.append((int(imdb_id),row.get('year')))
infile.close()

infile = open('master_test.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
for row in reader:
	imdb_id = row.get('imdb_id')[2:len(row.get('imdb_id'))]
	lot_movie.append((int(imdb_id),row.get('year')))
infile.close()

# trope list data
infile = open('tvt_work_trope_link.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_tropelist = []
for row in reader:
	lot_tropelist.append((row.get('work_tvt_id'),row.get('trope_tvt_id')))
infile.close()

# individual trope data
infile = open('trope.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_tropes = []
for row in reader:
	lot_tropes.append((row.get('tvt_id'),row.get('title').decode('utf-8')))
infile.close()

# IMDB to TVTropes links
infile = open('imdb_id_master.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
lot_link = []
for row in reader:
		lot_link.append((row.get('imdb_id'),row.get('tvt_id')))
infile.close()

con = sqlite.connect('tvt_timeseries.db')
cur = con.cursor()

# create tables
cur.execute("DROP TABLE IF EXISTS movie")
cur.execute("DROP TABLE IF EXISTS link")
cur.execute("DROP TABLE IF EXISTS tropelist")
cur.execute("DROP TABLE IF EXISTS tropes")
cur.execute("CREATE TABLE movie (imdb_id int, year int)")
cur.execute("CREATE TABLE link (imdb_id int, tvt_id int)")
cur.execute("CREATE TABLE tropelist (tvt_id int, trope_id int)")
cur.execute("CREATE TABLE tropes (tvt_id int, title varchar(255))")

# insert data into tables
cur.executemany("INSERT INTO movie VALUES (?,?)", lot_movie)
con.commit()
cur.executemany("INSERT INTO link VALUES (?,?)", lot_link)
con.commit()
cur.executemany("INSERT INTO tropelist VALUES (?,?)", lot_tropelist)
con.commit()
cur.executemany("INSERT INTO tropes VALUES (?,?)", lot_tropes)
con.commit()

outfile = open('tvt_timeseries_all.csv','w')
writer = csv.DictWriter(outfile,delimiter=',',fieldnames=['trope_id','trope_name','reg_coef'])
writer.writeheader()
# Loop through every trope
for trope in lot_tropes:
	trope_id = int(trope[0])
	trope_name = trope[1]
	# First SQL statement counts how many movies the trope appeared in (as recorded on TVT) per year
	cur.execute("SELECT movie.year, COUNT(*) FROM movie INNER JOIN link ON movie.imdb_id=link.imdb_id INNER JOIN tropelist ON tropelist.tvt_id=link.tvt_id WHERE tropelist.trope_id=? GROUP BY movie.year ORDER BY movie.year", (trope_id,))
	rows_trope = cur.fetchall()
	# Second SQL statement counts how many movies were released per year (that are included with accurate years in the data)
	cur.execute("SELECT movie.year, COUNT(*) FROM movie INNER JOIN link ON movie.imdb_id=link.imdb_id GROUP BY movie.year ORDER BY movie.year")
	rows_total = cur.fetchall()
	years = []
	ratios = []
	# Count movies released between 1900 and 2016
	for j in range(1900,2016):
		# Match count values for each year
		years.append(j)
		match1 = -1
		match2 = -1
		for k in range(0,len(rows_trope)):
			if rows_trope[k][0] == j:
				match1 = k
		for l in range(0,len(rows_total)):
			if rows_total[l][0] == j:
				match2 = l
		# If both counts were actually obtained for the year
		if match1 > -1 and match2 > -1:
			ratios.append((rows_trope[match1][1]*1.00)/(rows_total[match2][1]*1.00))
		# Otherwise one or more counts is zero
		else:
			ratios.append(0.00)
	regr = linear_model.LinearRegression()
	years = np.asarray(years).reshape(len(years),1)
	ratios = np.asarray(ratios)
	regr.fit(years,ratios)
	coef = regr.coef_[0]
	# Print statement is optional
	print 'Trope ID: %s | Trope Name: %s | Linear Regression Coefficient: %s' % (trope_id,trope_name,coef)
	writer.writerow({'trope_id':trope_id,'trope_name':trope_name.encode('ascii','ignore'),'reg_coef_train':coef})
outfile.close()
