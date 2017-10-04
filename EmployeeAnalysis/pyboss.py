import os
import csv
from employee import Employee

root_path = os.getcwd()
data_path = os.path.join(root_path,"raw_data")

def loadfiles():
	files = []
	for file in os.listdir(data_path):
		if file.endswith(".csv"):
			files.append(os.path.join(data_path, file))
	return files

files = loadfiles()

emp_list = []
for file in files:
	with open(file, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		csvdata = list(csvreader)
		for row in csvdata[1:]:
			emp = Employee(row[0], row[1],row[2],row[3],row[4])
			emp_list.append(emp.emp_dict)

output = os.path.join(root_path,"employee_processed.csv")
with open(output, "w") as csvfile:
    csvwriter = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=Employee.fieldNames)
    csvwriter.writeheader()
    csvwriter.writerows(emp_list)

