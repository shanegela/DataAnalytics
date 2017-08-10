import requests
import os
import csv
from bs4 import BeautifulSoup
from datetime import datetime

team_dict = {
	"New England":"NE",
	"Denver":"DEN",
	"Seattle":"SEA",
	"NY Giants":"NYG",
	"Minnesota":"MIN",
	"Kansas City":"KC",
	"Cincinnati":"CIN",
	"Dallas":"DAL",
	"Baltimore":"BAL",
	"Pittsburgh":"PIT",
	"Philadelphia":"PHI",
	"Houston":"HOU",
	"Detroit":"DET",
	"Arizona":"ARI",
	"Tampa Bay":"TB",
	"Tennessee":"TEN",
	"Buffalo":"BUF",
	"Washington":"WAS",
	"Miami":"MIA",
	"Oakland":"OAK",
	"Indianapolis":"IND",
	"LA Rams":"LAR",
	"Chicago":"CHI",
	"Jacksonville":"JAC",
	"Green Bay":"GB",
	"Carolina":"CAR",
	"Atlanta":"ATL",
	"NY Jets":"NYJ",
	"LA Chargers":"LAC",
	"Cleveland":"CLE",
	"New Orleans":"NO",
	"San Francisco":"SF"
}

url = "http://www.oddsshark.com/nfl/defensive-stats"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")
team_ranks =[]
table = soup.find("table",{"class":"base-table base-table-sortable"})
teams = table.find_all("tr")
rank = 1;
for team in teams:
	cols = team.find_all("td")
	team = ""
	if len(cols) > 0:
		#print(cols)
		for idx, col in enumerate(cols):
			if idx == 0:
				team = col.text.strip()
		#print(f"date: {date} rank: {rank} team: {team}")
		#print(team)
		if team in team_dict:
			team_abbr = team_dict[team]
			team_ranks.append({"Team": team_abbr, "Rank": rank})
			rank += 1
		else:
			print(f"not found {team}")

#print(team_ranks)
root_path = os.getcwd()
out_file = os.path.join(root_path, 'DefensiveTeamRank.csv')
with open(out_file,"w", newline="") as fh:
	fieldnames = ["Team","Rank"]
	csvwriter = csv.DictWriter(fh, fieldnames=fieldnames)
	csvwriter.writeheader()
	for team in team_ranks:
		csvwriter.writerow(team)