import sys
import re
import requests
from bs4 import BeautifulSoup

url = "https://atl-02.statsplus.net/tlg/reports/news/html/players/player_36536.html"
#url = "https://atl-02.statsplus.net/tlg/reports/news/html/players/player_57423.html"

player_id = re.search('https://atl-02.statsplus.net/tlg/reports/news/html/players/player_(.*).html', url)
player_id = player_id.group(1)
print(player_id)


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
# print(one_liner)
one_liner_list = one_liner.split()
pos = one_liner_list[0]
i = 1
name = ''
while not one_liner_list[i].startswith('#'):
    name = name + one_liner_list[i] + ' '
    i = i + 1
name = name.strip()
# print(name)

number=''
for x in one_liner_list:
    if x.startswith("#"):
        number = x[1:]


age = one_liner_list[one_liner_list.index('AGE:') + 1]
bats = one_liner_list[one_liner_list.index('BATS:') + 1]
throws = one_liner_list[one_liner_list.index('THROWS:') + 1]
morale_first = one_liner_list.index('MORALE:') + 1
morale_range = range(morale_first, len(one_liner_list))
# print(morale_range)
morale=''
for n in morale_range:
    morale = morale + one_liner_list[n] + ' '
morale = morale.strip()

print(team)
print(pos)
print(name)
print(number)
print(age)
print(bats)
print(throws)
print(morale)

### should be able to use the above for pitchers as well

batting_ratings = soup.find('td', string='Contact')
# print(batting_ratings)
skip1 = batting_ratings.find_next('td')
skip2 = skip1.find_next('td')
contact_overall_td = skip2.find_next('td')
contact_overall = contact_overall_td.text
contact_v_left_td = contact_overall_td.find_next('td')
contact_v_left = contact_v_left_td.text
contact_v_right_td = contact_v_left_td.find_next('td')
contact_v_right = contact_v_right_td.text
contact_potential_td = contact_v_right_td.find_next('td')
contact_potential = contact_potential_td.text
print(contact_overall)
print(contact_v_left)
print(contact_v_right)
print(contact_potential)

batting_ratings = soup.find('td', string='Gap')
# print(batting_ratings)
skip1 = batting_ratings.find_next('td')
skip2 = skip1.find_next('td')
gap_overall_td = skip2.find_next('td')
gap_overall = gap_overall_td.text
gap_v_left_td = gap_overall_td.find_next('td')
gap_v_left = gap_v_left_td.text
gap_v_right_td = gap_v_left_td.find_next('td')
gap_v_right = gap_v_right_td.text
gap_potential_td = gap_v_right_td.find_next('td')
gap_potential = gap_potential_td.text
print(gap_overall)
print(gap_v_left)
print(gap_v_right)
print(gap_potential)

batting_ratings = soup.find('td', string='Power')
skip1 = batting_ratings.find_next('td')
skip2 = skip1.find_next('td')
power_overall_td = skip2.find_next('td')
power_overall = power_overall_td.text
power_v_left_td = power_overall_td.find_next('td')
power_v_left = power_v_left_td.text
power_v_right_td = power_v_left_td.find_next('td')
power_v_right = power_v_right_td.text
power_potential_td = power_v_right_td.find_next('td')
power_potential = power_potential_td.text
print(power_overall)
print(power_v_left)
print(power_v_right)
print(power_potential)

batting_ratings = soup.find('td', string='Eye')
skip1 = batting_ratings.find_next('td')
skip2 = skip1.find_next('td')
eye_overall_td = skip2.find_next('td')
eye_overall = eye_overall_td.text
eye_v_left_td = eye_overall_td.find_next('td')
eye_v_left = eye_v_left_td.text
eye_v_right_td = eye_v_left_td.find_next('td')
eye_v_right = eye_v_right_td.text
eye_potential_td = eye_v_right_td.find_next('td')
eye_potential = eye_potential_td.text
print(eye_overall)
print(eye_v_left)
print(eye_v_right)
print(eye_potential)

batting_ratings = soup.find('td', string="Avoid K's")
skip1 = batting_ratings.find_next('td')
skip2 = skip1.find_next('td')
avoidK_overall_td = skip2.find_next('td')
avoidK_overall = avoidK_overall_td.text
avoidK_v_left_td = avoidK_overall_td.find_next('td')
avoidK_v_left = avoidK_v_left_td.text
avoidK_v_right_td = avoidK_v_left_td.find_next('td')
avoidK_v_right = avoidK_v_right_td.text
avoidK_potential_td = avoidK_v_right_td.find_next('td')
avoidK_potential = avoidK_potential_td.text
print(avoidK_overall)
print(avoidK_v_left)
print(avoidK_v_right)
print(avoidK_potential)

#print("Fielding")
fielding_ratings = soup.find('td', string='Range:')
# print(fielding_ratings)
catcher_range_td = fielding_ratings.find_next('td')
catcher_range = catcher_range_td.text
infield_range_td = catcher_range_td.find_next('td')
infield_range = infield_range_td.text
outfield_range_td = infield_range_td.find_next('td')
outfield_range = outfield_range_td.text
print(catcher_range)
print(infield_range)
print(outfield_range)

fielding_ratings = soup.find('td', string='Errors:')
# print(fielding_ratings)
catcher_errors_td = fielding_ratings.find_next('td')
catcher_errors = catcher_errors_td.text
infield_errors_td = catcher_errors_td.find_next('td')
infield_errors = infield_errors_td.text
outfield_errors_td = infield_errors_td.find_next('td')
outfield_errors = outfield_errors_td.text
print(catcher_errors)
print(infield_errors)
print(outfield_errors)

fielding_ratings = soup.find('td', string='Arm:')
# print(fielding_ratings)
catcher_arm_td = fielding_ratings.find_next('td')
catcher_arm = catcher_arm_td.text
infield_arm_td = catcher_arm_td.find_next('td')
infield_arm = infield_arm_td.text
outfield_arm_td = infield_arm_td.find_next('td')
outfield_arm = outfield_arm_td.text
print(catcher_arm)
print(infield_arm)
print(outfield_arm)

fielding_ratings = soup.find('td', string='Turn DP:')
# print(fielding_ratings)
catcher_turndp_td = fielding_ratings.find_next('td')
catcher_turndp = catcher_turndp_td.text
infield_turndp_td = catcher_turndp_td.find_next('td')
infield_turndp = infield_turndp_td.text
outfield_turndp_td = infield_turndp_td.find_next('td')
outfield_turndp = outfield_turndp_td.text
print(catcher_turndp)
print(infield_turndp)
print(outfield_turndp)

fielding_ratings = soup.find('td', string='Ability:')
# print(fielding_ratings)
catcher_ability_td = fielding_ratings.find_next('td')
catcher_ability = catcher_ability_td.text
infield_ability_td = catcher_ability_td.find_next('td')
infield_ability = infield_ability_td.text
outfield_ability_td = infield_ability_td.find_next('td')
outfield_ability = outfield_ability_td.text
print(catcher_ability)
print(infield_ability)
print(outfield_ability)

#data= soup.find_all('table')
#print(len(data))  # this is variable based on player


print('######################################################')
td_greg = soup.find_all('td')
pitcher_label = 0
pitcher_rating_loc = 0
for d in td_greg:
    if d.text == 'Pitcher:':
        pitcher_label=td_greg.index(d)
        break

pitcher_rating = td_greg[pitcher_label + 1].text
ss_rating = td_greg[pitcher_label +3].text
catcher_rating = td_greg[pitcher_label +5].text
lf_rating = td_greg[pitcher_label +7].text
firstbase_rating = td_greg[pitcher_label +9].text
cf_rating = td_greg[pitcher_label +11].text
secondbase_rating = td_greg[pitcher_label +13].text
rf_rating = td_greg[pitcher_label +15].text
thirdbase_rating = td_greg[pitcher_label +17].text
print(pitcher_rating)
print(ss_rating)
print(catcher_rating)
print(lf_rating)
print(firstbase_rating)
print(cf_rating)
print(secondbase_rating)
print(rf_rating)
print(thirdbase_rating)

rs = 0
sa=0
br=0
sb=0
bh=0

for d in td_greg:
    if d.text == 'Running Speed:':
        running_speed = td_greg[td_greg.index(d) + 1].text
    if d.text == 'Stealing Ability:':
        stealing_ability = td_greg[td_greg.index(d)+1].text
    if d.text == 'Baserunning Inst.:':
        baserunning = td_greg[td_greg.index(d)+1].text
    if d.text == 'Sacrifice Bunt:':
        sac_bunt = td_greg[td_greg.index(d) + 1].text
    if d.text == 'Bunt for Hit:':
        bunt_hit = td_greg[td_greg.index(d)+1].text
        break

print(running_speed)
print(stealing_ability)
print(baserunning)
print(sac_bunt)
print(bunt_hit)
