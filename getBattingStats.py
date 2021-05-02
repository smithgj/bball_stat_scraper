import sys
import re
import requests
from bs4 import BeautifulSoup

url = "https://atl-02.statsplus.net/tlg/reports/news/html/players/player_36536.html"
#url = "https://atl-02.statsplus.net/tlg/reports/news/html/players/player_57423.html"


batter_page = requests.get(url)
# print(page)
soup = BeautifulSoup(batter_page.content, 'html.parser')

team_name_pages = soup.find('a', {'class':'boxlink'},{'style':'font-weight:bold'})
team = team_name_pages['href']
# print(team)
team = re.search('../teams/team_(.*).html', team)
team = team.group(1)
# at this point team is the team_id number or "" for free agents

one_liner = soup.find('th', {'colspan':'2'},{'class':'boxtitle'} )
one_liner = one_liner.find('a')
one_liner = one_liner.text
# RF AARON 'ALL RISE' JUDGE #99 - AGE: 29 - BATS: R - THROWS: R - MORALE: VERY GOOD
# C TRENT JACKSON #5 - AGE: 21 - BATS: L - THROWS: R - MORALE: GOOD
print(one_liner)
one_liner_list = one_liner.split()
pos = one_liner_list[0]
i = 1
name = ''
while not one_liner_list[i].startswith('#'):
    name = name + one_liner_list[i] + ' '
    i = i + 1
name = name.strip()
print(name)
for x in one_liner_list:
    if x.startswith("#"):
        number = x[1:]

print(number)
