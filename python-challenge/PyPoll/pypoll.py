import os
import csv
from collections import Counter

root_path = os.getcwd()
data_path = os.path.join(root_path,"raw_data")

def loadfiles():
	files = []
	#files.append(os.path.join(data_path, "election_data_1.csv"))
	for file in os.listdir(data_path):
		if file.endswith(".csv"):
			files.append(os.path.join(data_path, file))
	return files


files = loadfiles()
# candidates = unique list of candidates
candidates = set()
cand_dict = dict()

for file in files:
	voters = []
	with open(file, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		csvdata = list(csvreader)
		#print(csvdata)
		for row in csvdata[1:]:
			candidates.add(row[2])
			voters.extend(row)
	#print(voters)
	voter_count = {}.fromkeys(voters,0)
	voter_count = Counter(voters)
	for candidate in candidates:
		if candidate in cand_dict:
			cand_dict[candidate] += voter_count[candidate]
		else:
			cand_dict.update({candidate: voter_count[candidate]})

total_votes = sum(cand_dict.values())
#print(total_votes)

max_votes = max(cand_dict.values())
# getting all keys containing the `maximum`
max_keys = [k for k, v in cand_dict.items() if v == max_votes] 
#print(max_votes, max_keys)

#candidate details
details = ""
for candidate, votes in cand_dict.items():
	pct_votes = votes/ total_votes * 100
	details += f"{candidate}: {'{:,.2f}%'.format(pct_votes)} ({ '{:,d}'.format(votes)})\n"
# winner
if (len(max_keys) > 1):
	tied = ", ".join(max_keys)
	winner = f"It's a tie! {tied}\n"
else:
	winner =f"Winner: {max_keys[0]}\n"

summary = (
	f"Election Results\n"
	f"---------------------------\n"
	f"Total Votes: {total_votes}\n"
	f"---------------------------\n"
	f"{details}"
	f"---------------------------\n"
	f"{winner}"
	f"---------------------------\n"
	)

# print summary to console
print(summary)

# print summary to output file
output = os.path.join(root_path, 'pypoll_out.txt')
with open(output, 'w') as fh:
	fh.write(summary)
