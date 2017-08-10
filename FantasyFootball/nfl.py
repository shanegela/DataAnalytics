#http://www.espn.com/fantasy/football/story/_/page/17RanksPreseasonBerryPPR/matthew-berry-2017-ppr-rankings-fantasy-football

import os
import csv
from lxml import html
import requests
from bs4 import BeautifulSoup

def getTeamCode(team):
	x = team.strip().upper()
	if x == "SD":
		return "LAC"
	elif x == "LA":
		return "LAR"
	elif x == "JAX":
		return "JAC"
	else:
		return x

players_list = []
# the lower the rank the better
url = 'http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticPositionCategory=QUARTERBACK&season=2016&seasonType=REG&experience=&tabSeq=1&qualified=true&Submit=Go'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'QB'
for table in soup.find_all('table'):
	for row in table.find_all('tr'):
		rank = None
		team = None
		name = None
		for idx, player in enumerate(row.find_all('td')):
			if idx == 0:
				rank = player.text.strip()
			if idx == 1:
				name = player.text.strip()
			if idx == 2:
				team = getTeamCode(player.text)
		if rank is not None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

url = 'http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticPositionCategory=RUNNING_BACK&season=2016&seasonType=REG&experience=&tabSeq=1&qualified=true&Submit=Go'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'RB'
for table in soup.find_all('table'):
	for row in table.find_all('tr'):
		rank = None
		team = None
		name = None
		for idx, player in enumerate(row.find_all('td')):
			if idx == 0:
				rank = player.text.strip()
			if idx == 1:
				name = player.text.strip()
			if idx == 2:
				team = getTeamCode(player.text)
		if rank is not None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)


url = 'http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticPositionCategory=WIDE_RECEIVER&season=2016&seasonType=REG&experience=&tabSeq=1&qualified=true&Submit=Go'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'WR'
for table in soup.find_all('table'):
	for row in table.find_all('tr'):
		rank = None
		team = None
		name = None
		for idx, player in enumerate(row.find_all('td')):
			if idx == 0:
				rank = player.text.strip()
			if idx == 1:
				name = player.text.strip()
			if idx == 2:
				team = getTeamCode(player.text)
		if rank is not None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

url = 'http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticPositionCategory=TIGHT_END&season=2016&seasonType=REG&experience=&tabSeq=1&qualified=true&Submit=Go'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'TE'
for table in soup.find_all('table'):
	for row in table.find_all('tr'):
		rank = None
		team = None
		name = None
		for idx, player in enumerate(row.find_all('td')):
			if idx == 0:
				rank = player.text.strip()
			if idx == 1:
				name = player.text.strip()
			if idx == 2:
				team = getTeamCode(player.text)
		if rank is not None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

url = 'http://www.nfl.com/stats/categorystats?archive=false&conference=null&statisticPositionCategory=FIELD_GOAL_KICKER&season=2016&seasonType=REG&experience=&tabSeq=1&qualified=true&Submit=Go'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'K'
for table in soup.find_all('table'):
	for row in table.find_all('tr'):
		rank = None
		team = None
		name = None
		for idx, player in enumerate(row.find_all('td')):
			if idx == 0:
				rank = player.text.strip()
			if idx == 1:
				name = player.text.strip()
			if idx == 2:
				team = getTeamCode(player.text)
		if rank is not None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

root_path = os.getcwd()
out_file = os.path.join(root_path, 'NFL.csv')
with open(out_file,"w", newline="") as fh:
	csvwriter = csv.writer(fh,delimiter=",")
	csvwriter.writerow(["Team","Position","Name","Rank"])
	csvwriter.writerows(players_list)



