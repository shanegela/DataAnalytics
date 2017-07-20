import requests
import os
import csv
from bs4 import BeautifulSoup
from datetime import datetime

root_url = "http://www.espn.com"

sched_url = root_url + "/nfl/schedule"
sched_page = requests.get(sched_url)
sched_soup = BeautifulSoup(sched_page.text, "lxml")

game_list =[]
weeks = sched_soup.find("div", {"class": "mobile-dropdown dropdown-type-week"}).find_all("option")
for week in weeks:
	#print(week.text)
	the_week = week.text
	week_url = root_url + (week["data-url"])
	week_page = requests.get(week_url)
	week_soup = BeautifulSoup(week_page.text,"lxml")
	sched = week_soup.find('div', id='sched-container')
	tables = sched.find_all("tbody")
	dates = sched.find_all("h2")
	for idx, table in enumerate(tables):
		game_day = (dates[idx].text)
		_, month = game_day.split(', ')
		month = month + " 2017"
		game_date = datetime.strptime(month, '%B %d %Y')
		game_date_str = game_date.strftime('%m/%d/%Y')
		rows = table.find_all("tr")
		for row in rows:
			#print(row)
			team1 = "error"
			team2 = "error"
			team1_abbr = "error"
			team2_abbr = "error"
			teams = row.find_all("span")
			if (len(teams) > 0):
				team1 = teams[0].text
				team2 = teams[1].text
			abbrs = row.find_all("abbr")
			if (len(abbrs) > 0):
				team1_abbr = abbrs[0].text
				team2_abbr = abbrs[1].text
			#print(f"week: {the_week} Day: {game_day} team1: {team1} ({team1_abbr}) team2: {team2} ({team2_abbr})")
			game_list.append({"week": the_week, "day": game_date_str, "team1": team1, "team1_abbr": team1_abbr, "team2": team2, "team2_abbr": team2_abbr})	

#print(game_list)
root_path = os.getcwd()
out_file = os.path.join(root_path, 'game_sched.csv')
with open(out_file,"w", newline="") as fh:
	fieldnames = ["week","day","team1","team1_abbr","team2","team2_abbr"]
	csvwriter = csv.DictWriter(fh, fieldnames=fieldnames)
	csvwriter.writeheader()
	for game in game_list:
		csvwriter.writerow(game)