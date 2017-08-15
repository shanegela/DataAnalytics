# 2 attempt at pybank

#importing libraries

import os
import csv

#establish rootpath and file path
rootpath = os.getcwd()
#print(rootpath)
file = os.path.join(rootpath, 'raw_data/budget_data_1.csv')
#print(filepath)

'''trying to read one line from file

with open(filepath, 'r') as fh:
	 trying to read lines from csv file
	# line = fh.readline()
	# print(line)
	#for line in fh:
		#print(line, end='')
	'''

#opening csv file in read format	

with open (file, 'r') as infile:
	#no_months = []
	#csvreader = csv.reader(infile, delimiter = ',')
	csvreader = csv.reader(infile)
	#print(csvreader)
	header = next(csvreader)
	#print(header)
	csvdata = list(csvreader)
	#print(csvdata)
	no_months = len(csvdata)
	#print(no_months)
	#adding values of budget
	#total = 0
	#for r in csvdata:
	total = sum(int(r[1]) for r in csvdata)
	#print(total)
	#average
	rev_avg = round(total/no_months,0)
	#print(rev_avg)
	increase = 0
	for idx, row in enumerate(csvdata):
		#print(int)
		if idx == 0:
			prev_val = float(row[1])
		else:
			curr_val = float(row[1])
			chg_val = curr_val - prev_val
			if (chg_val > increase):
				increase = chg_val
	print(increase)







# #----------------------------
# #printing output to text file.
# output_path = os.path.join(os.getcwd(),'output.txt')
# #print(output_path)
# with open(output_path, 'w') as outfile:
# 	fw.write("Financial Analysis\n")
# 	fw.write("-------------------------\n")
# 	fw.write(f"Total Months: {no_months}\n" )