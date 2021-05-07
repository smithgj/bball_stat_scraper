import sys
import re
import requests
from bs4 import BeautifulSoup
from getBattingStats import get_batter_data




url = "https://atl-02.statsplus.net/tlg/reports/news/html/leagues/league_153_players.html"
base_url = "https://atl-02.statsplus.net/tlg/reports/news/html"

start_page = requests.get(url)
# print(page)
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
#    print(a['href'])
    player_page_end_url = a['href'].strip('.')
    #print(player_page_end_url)
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


def extract_data(soup, player_id):
    #get page
    #if position player
        #extract position data
    #else
        #extract pitcher data
    data_dict = get_batter_data(soup, player_id)
    return(data_dict)

#def persist_data()


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
    # print(one_liner)
    one_liner_list = one_liner.split()
    pos = one_liner_list[0]
    if pos != 'P':
        player_dict = extract_data(soup, player_id)
        # persist_data()
        print(player_dict)
    else:
        print("must be a pitcher")




#def extract_position_data() - getBattingStats - separate file

#def extract_pitching_data() - getPitchingStats -separate file