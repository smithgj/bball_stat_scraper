import sys
import re
import requests
from bs4 import BeautifulSoup


def get_batter_data():


    url = "https://atl-02.statsplus.net/tlg/reports/news/html/players/player_36536.html"
     # url = "https://atl-02.statsplus.net/tlg/reports/news/html/players/player_57423.html"

    player_id = re.search('https://atl-02.statsplus.net/tlg/reports/news/html/players/player_(.*).html', url)
    player_id = player_id.group(1)
    batter_data = {
        "player_id" : player_id
    }

    batter_page = requests.get(url)
    soup = BeautifulSoup(batter_page.content, 'html.parser')

    team_name_pages = soup.find('a', {'class': 'boxlink'}, {'style': 'font-weight:bold'})
    team = team_name_pages['href']
    # print(team)
    team = re.search('../teams/team_(.*).html', team)
    team = team.group(1)
    # at this point team is the team_id number or "" for free agents
    batter_data.update({"team_id": team})

    one_liner = soup.find('th', {'colspan': '2'}, {'class': 'boxtitle'})
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
    batter_data.update({
        "position" : pos,
        "player_name": name
    })

    number = ''
    for x in one_liner_list:
        if x.startswith("#"):
            number = x[1:]

    age = one_liner_list[one_liner_list.index('AGE:') + 1]
    bats = one_liner_list[one_liner_list.index('BATS:') + 1]
    throws = one_liner_list[one_liner_list.index('THROWS:') + 1]
    morale_first = one_liner_list.index('MORALE:') + 1
    morale_range = range(morale_first, len(one_liner_list))
    # print(morale_range)
    morale = ''
    for n in morale_range:
        morale = morale + one_liner_list[n] + ' '
    morale = morale.strip()

    batter_data.update( {
        "number": number,
        "age": age,
        "bats": bats,
        "throws":throws,
        "morale":morale
    })


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
    batter_data.update({
        "contact_ovr": contact_overall,
        "contact_vs_left": contact_v_left,
        "contact_vs_right": contact_v_right,
        "contact_pot": contact_potential
    })
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
    batter_data.update({
        "gap_ovr": gap_overall,
        "gap_vs_left": gap_v_left,
        "gap_vs_right": gap_v_right,
        "gap_pot": gap_potential
    })

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

    batter_data.update({
        "pwr_ovr": power_overall,
        "pwr_vs_left": power_v_left,
        "pwr_vs_right": power_v_right,
        "pwr_pot": power_potential
    })

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
    batter_data.update({
        "eye_ovr": eye_overall,
        "eye_vs_left": eye_v_left,
        "eye_vs_right": eye_v_right,
        "eye_pot": eye_potential
    })

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
    batter_data.update({
        "avoidK_ovr": avoidK_overall,
        "avoidK_vs_left": avoidK_v_left,
        "avoidK_vs_right": avoidK_v_right,
        "avoidK_pot": avoidK_potential
    })

    # print("Fielding")
    fielding_ratings = soup.find('td', string='Range:')
    # print(fielding_ratings)
    catcher_range_td = fielding_ratings.find_next('td')
    catcher_range = catcher_range_td.text
    infield_range_td = catcher_range_td.find_next('td')
    infield_range = infield_range_td.text
    outfield_range_td = infield_range_td.find_next('td')
    outfield_range = outfield_range_td.text

    batter_data.update({
        "catcher_range": catcher_range,
        "infield_range": infield_range,
        "outfield_range": outfield_range
    })

    fielding_ratings = soup.find('td', string='Errors:')
    # print(fielding_ratings)
    catcher_errors_td = fielding_ratings.find_next('td')
    catcher_errors = catcher_errors_td.text
    infield_errors_td = catcher_errors_td.find_next('td')
    infield_errors = infield_errors_td.text
    outfield_errors_td = infield_errors_td.find_next('td')
    outfield_errors = outfield_errors_td.text
    batter_data.update({
        "catcher_errors": catcher_errors,
        "infield_errors": infield_errors,
        "outfield_errors": outfield_errors
    })

    fielding_ratings = soup.find('td', string='Arm:')
    # print(fielding_ratings)
    catcher_arm_td = fielding_ratings.find_next('td')
    catcher_arm = catcher_arm_td.text
    infield_arm_td = catcher_arm_td.find_next('td')
    infield_arm = infield_arm_td.text
    outfield_arm_td = infield_arm_td.find_next('td')
    outfield_arm = outfield_arm_td.text
    batter_data.update({
        "catcher_arm": catcher_arm,
        "infield_arm": infield_arm,
        "outfield_arm": outfield_arm
    })

    fielding_ratings = soup.find('td', string='Turn DP:')
    # print(fielding_ratings)
    catcher_turndp_td = fielding_ratings.find_next('td')
    catcher_turndp = catcher_turndp_td.text
    infield_turndp_td = catcher_turndp_td.find_next('td')
    infield_turndp = infield_turndp_td.text
    outfield_turndp_td = infield_turndp_td.find_next('td')
    outfield_turndp = outfield_turndp_td.text
    batter_data.update({
        "catcher_turndp": catcher_turndp,
        "infield_turndp": infield_turndp,
        "outfield_turndp": outfield_turndp
    })

    fielding_ratings = soup.find('td', string='Ability:')
    # print(fielding_ratings)
    catcher_ability_td = fielding_ratings.find_next('td')
    catcher_ability = catcher_ability_td.text
    infield_ability_td = catcher_ability_td.find_next('td')
    infield_ability = infield_ability_td.text
    outfield_ability_td = infield_ability_td.find_next('td')
    outfield_ability = outfield_ability_td.text
    batter_data.update({
        "catcher_ability": catcher_ability,
        "infield_ability": infield_ability,
        "outfield_ability": outfield_ability
    })

    # data= soup.find_all('table')
    # print(len(data))  # this is variable based on player

    td_greg = soup.find_all('td')
    pitcher_label = 0
    pitcher_rating_loc = 0
    for d in td_greg:
        if d.text == 'Pitcher:':
            pitcher_label = td_greg.index(d)
            break

    pitcher_rating = td_greg[pitcher_label + 1].text
    ss_rating = td_greg[pitcher_label + 3].text
    catcher_rating = td_greg[pitcher_label + 5].text
    lf_rating = td_greg[pitcher_label + 7].text
    firstbase_rating = td_greg[pitcher_label + 9].text
    cf_rating = td_greg[pitcher_label + 11].text
    secondbase_rating = td_greg[pitcher_label + 13].text
    rf_rating = td_greg[pitcher_label + 15].text
    thirdbase_rating = td_greg[pitcher_label + 17].text
    batter_data.update({
        "pitcher_rating": pitcher_rating,
        "ss_rating": ss_rating,
        "catcher_rating": catcher_rating,
        "lf_rating": lf_rating,
        "firstbase_rating": firstbase_rating,
        "cf_rating": cf_rating,
        "secondbase_rating": secondbase_rating,
        "rf_rating": rf_rating,
        "thirdbase_rating": thirdbase_rating
    })

    rs = 0
    sa = 0
    br = 0
    sb = 0
    bh = 0

    for d in td_greg:
        if d.text == 'Running Speed:':
            running_speed = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Stealing Ability:':
            stealing_ability = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Baserunning Inst.:':
            baserunning = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Sacrifice Bunt:':
            sac_bunt = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Bunt for Hit:':
            bunt_hit = td_greg[td_greg.index(d) + 1].text
            break

    batter_data.update({
        "running_speed": running_speed,
        "stealing_ability": stealing_ability,
        "baserunning": baserunning,
        "sac_bunt": sac_bunt,
        "bunt_hit": bunt_hit
    })
    personality_header = soup.find('th', string='PERSONALITY')
    personality = personality_header.find_next('td')
    per_com1 = personality.text
    skip3 = personality.find_next('td')
    per_com2 = (skip3.find_next('td')).text
    batter_data.update({
        "per_com1": per_com1,
        "per_com2": per_com2
    })


    for d in td_greg:
        if d.text == 'Birthday:':
            birthday = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Born in:':
            born_in = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Nationality:':
            nationality = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Height:':
            height = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Weight:':
             weight = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Local Popularity:':
            local_pop = td_greg[td_greg.index(d) + 1].text
        if d.text == 'National Pop.:':
            nat_pop = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Contract:':
            contract = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Salary:':
            salary = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Signed Through:':
            signed_thru = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Major Service:':
            maj_service = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Service This Yr:':
            serv_this_yr = td_greg[td_greg.index(d) + 1].text
        if d.text == '40-Man Service:':
            forty_man_serv = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Pro Service:':
            pro_serv = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Arbitration Eligibility:':
            arb_eligibility = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Option Years:':
            opt_yrs = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Contract Extension:':
            cont_ext = td_greg[td_greg.index(d) + 1].text
        if d.text == 'Drafted:':
            drafted = td_greg[td_greg.index(d) + 1].text

    batter_data.update({
        "birthday": birthday,
        "born_in": born_in,
        "nationality": nationality,
        "height": height,
        "weight": weight,
        "local_pop": local_pop,
        "nat_pop": nat_pop,
        "contract": contract,
        "salary": salary,
        "signed_thru": signed_thru,
        "maj_service": maj_service,
        "serv_this_yr": serv_this_yr,
        "forty_man_serv": forty_man_serv,
        "pro_serv": pro_serv,
        "arb_eligibility": arb_eligibility,
        "opt_yrs": opt_yrs,
        "cont_ext": cont_ext,
        "drafted": drafted
    })

    return batter_data