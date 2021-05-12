import sys
import re
import requests
import mysql.connector
import time
from datetime import datetime
from bs4 import BeautifulSoup

url = "https://atl-02.statsplus.net/tlg/reports/news/html/leagues/league_153_players.html"
base_url = "https://atl-02.statsplus.net/tlg/reports/news/html"

start_page = requests.get(url)
soup = BeautifulSoup(start_page.content, 'html.parser')
last_name_pages = soup.find('td', {'class':'boxtitle'})
# print(last_name_pages)  <a href="../leagues/league_153_players_b.html">B</a>

# gets rid of extra lines between valid anchors:
last_name_hrefs = last_name_pages.find_all('a')
# print(type(last_name_hrefs))  #it is a ResultSet
# print(last_name_hrefs[3]) <a href="../leagues/league_153_players_d.html">D</a>

#urls for player pages A thru Z:
player_pages_urls = []

# the following yields 26 lines like: ../leagues/league_153_players_w.html
#  so we will strip off the ".." and prepend the base_url
for a in last_name_hrefs:
    player_page_end_url = a['href'].strip('.')
    player_pages_urls.append(base_url + player_page_end_url)

players = []
for page in player_pages_urls:
    # print(page)
    player_page = requests.get(page)
    player_list_soup = BeautifulSoup(player_page.content, 'html.parser')
    all_anchors = player_list_soup.find('table', {'class':'data sortable'})
    all_hrefs = all_anchors.find_all('a')
    for b in all_hrefs:
        page_end_url = b['href'].strip('.')
        if "players" in page_end_url:
            players.append(base_url + page_end_url)

print('total number of players found = ' + str(len(players)))

# debug to print out all urls of individual player pages
#with open('player_pages.txt', 'w') as f:
#    for i in players:
#        print(i, file=f)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="bn7999hd",
    database="smitty"
)
mycursor = mydb.cursor()

today =  datetime.today().strftime('%Y-%m-%d')

# for each url in the players link list:
for player_url in players:
    player_id = re.search('https://atl-02.statsplus.net/tlg/reports/news/html/players/player_(.*).html', player_url)
    player_id = player_id.group(1)

    page = requests.get(player_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    one_liner = soup.find('th', {'colspan': '2'}, {'class': 'boxtitle'})
    one_liner = one_liner.find('a')
    one_liner = one_liner.text
    # RF AARON 'ALL RISE' JUDGE #99 - AGE: 29 - BATS: R - THROWS: R - MORALE: VERY GOOD
    # C TRENT JACKSON #5 - AGE: 21 - BATS: L - THROWS: R - MORALE: GOOD
    one_liner_list = one_liner.split()
    pos = one_liner_list[0]
    if pos != 'P':
        batter = {}
        team_name_pages = soup.find('a', {'class': 'boxlink'}, {'style': 'font-weight:bold'})
        team = team_name_pages['href']
        team = re.search('../teams/team_(.*).html', team)
        team = team.group(1)
        batter.update({"team_id": team, "player_id":player_id,"date":today})

        stat_table = soup.find('table', attrs={'class':'data', 'width':'673px', 'style':'margin-bottom:5px;'})
        first_row = stat_table.find("tr")
        second_row = first_row.find_next("tr")
        cells = second_row.findAll("td")
        games = cells[0].text
        ab = cells[1].text
        h = cells[2].text
        doubles = cells[3].text
        triples = cells[4].text
        hr = cells[5].text
        rbi = cells[6].text
        bb = cells[7].text
        k = cells[8].text
        avg = cells[9].text
        obp = cells[10].text
        slg = cells[11].text
        sb = cells[12].text
        war = cells[13].text

        batter.update({
            "games": games,
            "ab": ab,
            "h": h,
            "2b": doubles,
            "3b":triples,
            "hr":hr,
            "rbi": rbi,
            "bb":bb,
            "k":k,
            "avg":avg,
            "obp": obp,
            "slg":slg,
            "sb":sb,
            "war":war
        })

        sql = (
            "INSERT INTO batter_data (player_id, team_id, date, games, ab, "
            "h, 2b, 3b, hr, rbi, bb, k, avg, obp, slg, sb, war)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        data = (batter.get('player_id'), batter.get('team_id'), batter.get('date'),
                batter.get('games'), batter.get('ab'), batter.get('h'), batter.get('2b'),
                batter.get('3b'), batter.get('hr'), batter.get('rbi'), batter.get('bb'),
                batter.get('k'), batter.get('avg'), batter.get('obp'), batter.get('slg'),
                batter.get('sb'), batter.get('war'))

        try:
            mycursor.execute(sql, data)
            mydb.commit()
            print(mycursor.rowcount, "table: batter_data - record inserted.")

        except Exception as e:
            mydb.rollback()
            log = 'nightly_error' + today + '.log'
            ts = time.time()
            sttime = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
            with open(log, 'a') as logfile:
                logfile.write(sttime + "failed to insert record for " + batter.get('player_id') + '\n')
                logfile.write(sttime + str(e) + '\n')


    if pos == 'P':
        pitcher = {}
        team_name_pages = soup.find('a', {'class': 'boxlink'}, {'style': 'font-weight:bold'})
        team = team_name_pages['href']
        team = re.search('../teams/team_(.*).html', team)
        team = team.group(1)
        pitcher.update({"team_id": team, "player_id": player_id, "date": today})

        stat_table = soup.find('table', attrs={'class': 'data', 'width': '673px', 'style': 'margin-bottom:5px;'})
        first_row = stat_table.find("tr")
        second_row = first_row.find_next("tr")
        cells = second_row.findAll("td")
        games = cells[0].text
        games_started = cells[1].text
        record = cells[2].text
        saves = cells[3].text
        era = cells[4].text
        ip = cells[5].text
        ha = cells[6].text
        hr = cells[7].text
        bb = cells[8].text
        k = cells[9].text
        whip = cells[10].text
        war = cells[11].text

        record_str = record.split('-')
        wins = record_str[0]
        losses = record_str[1]

        pitcher.update({
            "games": games,
            "games_started": games_started,
            "wins": wins,
            "losses": losses,
            "saves": saves,
            "era": era,
            "ip": ip,
            "ha": ha,
            "hr": hr,
            "bb": bb,
            "k": k,
            "whip": whip,
            "war": war
        })

        sql = (
            "INSERT INTO pitcher_data (player_id, team_id, date, games, games_started, "
            "wins, losses, saves, era, ip, ha, hr, bb, k, whip, war)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
         )

        data = (pitcher.get('player_id'), pitcher.get('team_id'), pitcher.get('date'),
                pitcher.get('games'), pitcher.get('games_started'), pitcher.get('wins'), pitcher.get('losses'),
                pitcher.get('saves'), pitcher.get('era'), pitcher.get('ip'), pitcher.get('ha'),
                pitcher.get('hr'), pitcher.get('bb'), pitcher.get('k'), pitcher.get('whip'),
                pitcher.get('war'))

        try:
            mycursor.execute(sql, data)
            mydb.commit()
            print(mycursor.rowcount, "table: pitcher_data - record inserted.")

        except Exception as e:
            mydb.rollback()
            log = 'nightly_error' + today + '.log'
            ts = time.time()
            sttime = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
            with open(log, 'a') as logfile:
                logfile.write(sttime + "failed to insert record for " + pitcher.get('player_id') + '\n')
                logfile.write(sttime + str(e) + '\n')






