#http://www.espn.com/fantasy/football/story/_/page/17RanksPreseasonBerryPPR/matthew-berry-2017-ppr-rankings-fantasy-football

import os
import csv
from lxml import html
import requests
from bs4 import BeautifulSoup

players_list = []
# the lower the rank the better
url = 'http://www.footballdb.com/fantasy-football/index.html?pos=QB&yr=2016&wk=all&rules=1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'QB'
for table in soup.find_all('table'):
	for rowidx, row in enumerate(table.find_all('tr')):
		rank = rowidx-1
		team = None
		name = None
		player = row.find('td')
		if player != None:
			#print(f"player: {player}")
			player_name = player.find('span')
			if player_name != None:
				#print(f"name: {player_name.text}")
				x = player_name.text.split(', ')
				name= x[0]
				team = x[1]
		if name != None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

url = 'http://www.footballdb.com/fantasy-football/index.html?pos=RB&yr=2016&wk=all&rules=1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'RB'
for table in soup.find_all('table'):
	for rowidx, row in enumerate(table.find_all('tr')):
		rank = rowidx-1
		team = None
		name = None
		player = row.find('td')
		if player != None:
			#print(f"player: {player}")
			player_name = player.find('span')
			if player_name != None:
				#print(f"name: {player_name.text}")
				x = player_name.text.split(', ')
				name= x[0]
				team = x[1]
		if name != None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)


url = 'http://www.footballdb.com/fantasy-football/index.html?pos=WR&yr=2016&wk=all&rules=1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'WR'
for table in soup.find_all('table'):
	for rowidx, row in enumerate(table.find_all('tr')):
		rank = rowidx-1
		team = None
		name = None
		player = row.find('td')
		if player != None:
			#print(f"player: {player}")
			player_name = player.find('span')
			if player_name != None:
				#print(f"name: {player_name.text}")
				x = player_name.text.split(', ')
				name= x[0]
				team = x[1]
		if name != None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

url = 'http://www.footballdb.com/fantasy-football/index.html?pos=TE&yr=2016&wk=all&rules=1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'TE'
for table in soup.find_all('table'):
	for rowidx, row in enumerate(table.find_all('tr')):
		rank = rowidx-1
		team = None
		name = None
		player = row.find('td')
		if player != None:
			#print(f"player: {player}")
			player_name = player.find('span')
			if player_name != None:
				#print(f"name: {player_name.text}")
				x = player_name.text.split(', ')
				name= x[0]
				team = x[1]
		if name != None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)

url = 'http://www.footballdb.com/fantasy-football/index.html?pos=K&yr=2016&wk=all&rules=1'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

pos = 'K'
for table in soup.find_all('table'):
	for rowidx, row in enumerate(table.find_all('tr')):
		rank = rowidx-1
		team = None
		name = None
		player = row.find('td')
		if player != None:
			#print(f"player: {player}")
			player_name = player.find('span')
			if player_name != None:
				#print(f"name: {player_name.text}")
				x = player_name.text.split(', ')
				name= x[0]
				team = x[1]
		if name != None:
			#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
			player_list =[team, pos, name, rank]
			players_list.append(player_list)


root_path = os.getcwd()
out_file = os.path.join(root_path, 'footballdb.csv')
with open(out_file,"w", newline="") as fh:
	csvwriter = csv.writer(fh,delimiter=",")
	csvwriter.writerow(["team","position","name","rank"])
	csvwriter.writerows(players_list)



