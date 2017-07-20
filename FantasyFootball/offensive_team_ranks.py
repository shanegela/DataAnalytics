import requests
import os
import csv
from bs4 import BeautifulSoup
from datetime import datetime

url = "http://www.oddsshark.com/nfl/offensive-stats"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

team_ranks =[]
table = soup.find("table",{"class":"base-table base-table-sortable"})
teams = table.find_all("tr")
for team in teams:
	cols = team.find_all("td")
	team = ""
	rank = ""
	if len(cols) > 0:
		#print(cols)
		for idx, col in enumerate(cols):
			if idx == 0:
				team = col.text
			if idx == 1:
				rank = col.text
		now = datetime.now()
		date = f"{now.month}/{now.day}/{now.year}"
		#print(f"date: {date} rank: {rank} team: {team}")
		team_ranks.append({"date": date , "team": team, "rank": float(rank)})

#print(team_ranks)
root_path = os.getcwd()
out_file = os.path.join(root_path, 'offensive_team_ranks.csv')
with open(out_file,"w", newline="") as fh:
	fieldnames = ["date","team","rank"]
	csvwriter = csv.DictWriter(fh, fieldnames=fieldnames)
	csvwriter.writeheader()
	for team in team_ranks:
		csvwriter.writerow(team)