import requests
import os
import csv
from bs4 import BeautifulSoup

players_list = []
ppf_url = 'https://www.profootballfocus.com'

teams_url = ppf_url + '/nfl/teams'
teams_page = requests.get(teams_url)
teams_soup = BeautifulSoup(teams_page.text, 'lxml')

teams = teams_soup.find_all('a', href=True)
for team in teams:
	team_url = team['href']
	if ('/nfl/teams/' in team_url):
		team_url = ppf_url + team_url + "/roster"
		#print(team_url)
		team_page = requests.get(team_url)
		team_soup = BeautifulSoup(team_page.text,'lxml')
		players = team_soup.find_all('a', href=True)
		for player in players:
			player_url = player['href']
			if ('/nfl/players' in player_url):
				#print(player_url)
				player_url = ppf_url + player_url
				player_page = requests.get(player_url)
				player_soup = BeautifulSoup(player_page.text,'lxml')
				
				player_title = player_soup.title.string.split(" | ")
				temp = player_title[1]
				temp_sp_idx = temp.rfind(' ')
				team = temp[:temp_sp_idx]
				position = temp[temp_sp_idx+1:]
				name = player_soup.h1.find_all('span')[-1].string
				grades = player_soup.body.findAll(text='2016 PFF Grades')
				if len(grades) > 0:
					rank = float(player_soup.table.tr.find_all('td')[1].string)
				else:
					rank = 99999999999999

				#print(f"team: {team} position: {position} player name: {name} rank: {rank}")
				player_list =[team, position, name, rank]
				players_list.append(player_list)

root_path = os.getcwd()
out_file = os.path.join(root_path, 'ppf.csv')
with open(out_file,"w", newline="") as fh:
	csvwriter = csv.writer(fh,delimiter=",")
	csvwriter.writerow(["team","position","name","rank"])
	csvwriter.writerows(players_list)
