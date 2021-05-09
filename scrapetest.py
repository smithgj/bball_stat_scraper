import sys
import re
import requests
import mysql.connector
import time
from datetime import datetime
from bs4 import BeautifulSoup

player_url ='https://atl-02.statsplus.net/tlg/reports/news/html/players/player_45928.html'
page = requests.get(player_url)
soup = BeautifulSoup(page.content, 'html.parser')

batting_ratings = soup.find('td', string='Contact')

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

batting_ratings = soup.find('td', string='Gap')
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

batting_ratings = soup.find('td', string='Power')
print(batting_ratings)
skip1 = batting_ratings.find_next('td')
skip2 = skip1.find_next('td')
power_overall_td = skip2.find_next('td')
power_overall = power_overall_td.text
print(power_overall)
power_v_left_td = power_overall_td.find_next('td')
power_v_left = power_v_left_td.text
print(power_v_left)
power_v_right_td = power_v_left_td.find_next('td')
power_v_right = power_v_right_td.text

power_potential_td = power_v_right_td.find_next('td')
power_potential = power_potential_td.text
