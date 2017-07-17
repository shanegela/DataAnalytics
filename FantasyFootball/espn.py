#http://www.espn.com/fantasy/football/story/_/page/17RanksPreseasonBerryPPR/matthew-berry-2017-ppr-rankings-fantasy-football

import os
import csv
from lxml import html
import requests
from bs4 import BeautifulSoup

players_list = []
# the lower the rank the better
url = 'http://www.espn.com/fantasy/football/story/_/page/17RanksPreseasonBerryPPR/matthew-berry-2017-ppr-rankings-fantasy-football'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

for table in soup.find_all('table'):
	caption = table.find('caption')
	if ('quarterbacks' in caption.string):
		pos = 'QB'
	elif ('running backs' in caption.string):
		pos = 'RB'
	elif ('wide receivers' in caption.string):
		pos = 'WR'
	elif ('tight ends' in caption.string):
		pos = 'TE'
	elif ('kickers' in caption.string):
		pos = 'K'
	else:
		pos = 'skip'

	if (pos != 'skip'):
		for row in table.find_all('tr'):
			th = row.find('th')
			if (th is None): #not a table header
				for idx, player in enumerate(row.find_all('td')):
					if idx == 0:
						x = player.text.split('. ')
						rank = x[0]
						name = x[1]
					if idx == 1:
						team = player.text
				#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
				player_list =[team, pos, name, rank]
				players_list.append(player_list)


root_path = os.getcwd()
out_file = os.path.join(root_path, 'espn.csv')
with open(out_file,"w", newline="") as fh:
	csvwriter = csv.writer(fh,delimiter=",")
	csvwriter.writerow(["team","position","name","rank"])
	csvwriter.writerows(players_list)



