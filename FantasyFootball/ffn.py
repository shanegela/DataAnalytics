import os
import csv
from lxml import html
import requests
from bs4 import BeautifulSoup

players_list = []
# the lower the rank the better
qb_url = 'https://www.fantasyfootballnerd.com/fantasy-football-draft-rankings/QB'
rb_url = 'https://www.fantasyfootballnerd.com/fantasy-football-draft-rankings/RB'
wr_url = 'https://www.fantasyfootballnerd.com/fantasy-football-draft-rankings/WR'
te_url = 'https://www.fantasyfootballnerd.com/fantasy-football-draft-rankings/TE'
def_url = 'https://www.fantasyfootballnerd.com/fantasy-football-draft-rankings/DEF'
k_url = 'https://www.fantasyfootballnerd.com/fantasy-football-draft-rankings/K'

urls = dict([('QB', qb_url), ('RB', rb_url), ('WR', wr_url), ('TE', te_url), ('DEF', def_url), ('K', k_url)])

for pos, url in urls.items():
	page = requests.get(url)
	#tree = html.fromstring(page.content)
	#player = tree.xpath('//tr/')
	soup = BeautifulSoup(page.text, 'lxml')
	for row in soup.find('table').find_all('tr'):
		for idx, player in enumerate(row.find_all('td')):
			if idx == 0:
				rank = player.text
			if idx == 1:
				name = player.text
			if idx == 2:
				team = player.text
		#print(f"team: {team} position: {pos} player name: {name} rank: {rank}")
		player_list =[team, pos, name, rank]
		players_list.append(player_list)


root_path = os.getcwd()
out_file = os.path.join(root_path, 'ffn.csv')
with open(out_file,"w", newline="") as fh:
	csvwriter = csv.writer(fh,delimiter=",")
	csvwriter.writerow(["team","position","name","rank"])
	csvwriter.writerows(players_list)
