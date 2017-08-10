# https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php
# fantasy pros

import requests
import os
import csv
from bs4 import BeautifulSoup
import re

players_list = []
url = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

rows = soup.find_all('tr',{'class':re.compile('^mpb-player')})
for row in rows:
	cols = row.find_all('td')
	rank = cols[0].text
	player = cols[1].text.rstrip()
	player_sp_idx = player.rfind(' ')
	team = player[player_sp_idx+1:]
	name = player[:player_sp_idx]
	pos = ''.join([i for i in cols[2].text if not i.isdigit()])

	#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
	player_list =[team, pos, name, rank]
	players_list.append(player_list)

root_path = os.getcwd()
out_file = os.path.join(root_path, 'fpro.csv')
with open(out_file,"w", newline="") as fh:
	csvwriter = csv.writer(fh,delimiter=",")
	csvwriter.writerow(["team","pos","name","rank"])
	csvwriter.writerows(players_list)
