import csv

# Import regression coefficients
infile = open('tvt_timeseries_all.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
reg = dict()
for row in reader:
	reg[str(row.get('trope_id'))] = float(row.get('reg_coef'))
infile.close()

# Import base training or test data (with binary 1/0 trope variables)
infile = open('master_test.csv','rU')
reader = csv.DictReader(infile,delimiter=',')
h = reader.fieldnames # Full header
t = h[19:len(h)] # Only the trope columns
nt = h[0:19] # All other columns that won't be changed

# Output to file
outfile = open('master_test_plus.csv','w')
writer = csv.DictWriter(outfile,delimiter=',',fieldnames=h)
writer.writeheader()
# rnum is optional to see progress in terminal
rnum = 1
for row in reader:
	newrow = dict()
	# Copy unaltered columns
	for col in nt:
		newrow[col] = row.get(col)
	# Multiply corresponding binary variable by trope's regression coefficient
	for trope in t:
		newrow[trope] = float(row.get(trope)) * reg[trope]
	writer.writerow(newrow)
	# Optional
	print 'Row %s Done' % rnum
	rnum+=1

infile.close()
outfile.close()
