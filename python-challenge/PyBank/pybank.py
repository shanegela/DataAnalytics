import os
import csv
from datetime import datetime

root_path = os.getcwd()
data_path = os.path.join(root_path,"raw_data")

def loadfiles():
	files = []
	for file in os.listdir(data_path):
		if file.endswith(".csv"):
			files.append(os.path.join(data_path, file))
	return files

def getDate(date_str):
	# expecting Jul-2017 or Jul-17
	dateParts = date_str.split("-")

	validDate = False
	now = datetime.now()
	date = datetime(now.year, now.month, now.day)
	
	if len(dateParts) > 2:
		print("Error parsing {date_str} to date.  Format dates as Jul-201")
		return validDate, date
	else:
		mth = dateParts[0]
		yr = dateParts[1]
	
	if (len(yr) == 2):
		try:
			date = datetime.strptime(date_str,'%b-%y')
			validDate = True
		except Exception as e:
			print(e)
	else:
		if (len(yr) == 4):
			try:
				date = datetime.strptime(date_str,'%b-%Y')
				validDate = True
			except Exception as e:
				print(e)
		else:
			print("Error parsing {date_str} to date.  Format dates as Jul-201")
	return validDate, date

rev_dict = dict()
files = loadfiles()

for file in files:
	with open(file) as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			validDate, date = getDate(row["Date"])
			revenue = float(row["Revenue"])
			if validDate:
				if date in rev_dict:
					rev_dict[date] += revenue
				else:
					rev_dict.update({date: revenue})				


# The total number of months included in the dataset
cntmths = len(rev_dict)

# The total amount of revenue gained over the entire period
totrev = sum(rev_dict.values())

# The average change in revenue between months over the entire period
# The greatest increase in revenue (date and amount) over the entire period
# The greatest decrease in revenue (date and amount) over the entire period

diff_dict = dict()

prev_value = 0
total_diff = 0
max_date = datetime.strptime('01/01/1900', "%m/%d/%Y").date()
max_diff = 0
min_date = datetime.strptime('01/01/1900', "%m/%d/%Y").date()
min_rev = 0
cnt = 0
for key, value in sorted(rev_dict.items()):
	#print(f"key: {key} value: {value}")
	if cnt == 0:
		max_date = key
		max_diff = 0
		min_date = key
		min_diff = 0
	else:
		diff = value - prev_value
		total_diff += diff
		if diff > max_diff:
			max_date = key
			max_diff = diff
		if diff < min_diff:
			min_date = key
			min_diff = diff

	prev_value = value
	cnt += 1

max_rev = rev_dict[max_date]
min_rev = rev_dict[min_date]

summary = (
	f"Financial Analysis\n"
	f"----------------------------\n"
	f"Total Months: {cntmths}\n"
	f"Total Revenue: ${ '{:,.2f}'.format(totrev) }\n"
	f"Average Revenue Change: ${'{:,.2f}'.format(totrev/cntmths) }\n"
	f"Greatest Increase in Revenue: {max_date.strftime('%b-%Y')} (${ '{:,.2f}'.format(max_rev) })\n"
	f"Greatest Decrease in Revenue: {min_date.strftime('%b-%Y')} (${ '{:,.2f}'.format(min_rev) })\n"
	)

# print summary to console
print(summary)

# print summary to output file
output = os.path.join(root_path, 'pybank_out.txt')
with open(output, 'w') as fh:
	fh.write(summary)