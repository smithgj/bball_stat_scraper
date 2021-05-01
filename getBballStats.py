import requests
from bs4 import BeautifulSoup

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

for page in player_pages_urls:
    print(page)
    # go to each page
    # get all player links and store in a list

# for each url in the players link list:
    # extract_data(url)

#def extract_data(url):
    #get page
    #extrat data
    #put in db