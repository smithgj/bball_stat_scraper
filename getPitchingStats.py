import sys
import re
import requests
from bs4 import BeautifulSoup


def get_pitcher_data(soup, player_id):

    pitcher_data = {
        "player_id" : player_id
    }

    team_name_pages = soup.find('a', {'class': 'boxlink'}, {'style': 'font-weight:bold'})
    team = team_name_pages['href']
    # print(team)
    team = re.search('../teams/team_(.*).html', team)
    team = team.group(1)
    # at this point team is the team_id number or "" for free agents
    pitcher_data.update({"team_id": team})

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
    pitcher_data.update({
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

    pitcher_data.update( {
        "number": number,
        "age": age,
        "bats": bats,
        "throws":throws,
        "morale":morale
    })


    ### should be able to use the above for pitchers as well

    pitching_ratings = soup.find('td', string='Stuff')
    # print(pitching_ratings)
    skip1 = pitching_ratings.find_next('td')
    skip2 = skip1.find_next('td')
    stuff_overall_td = skip2.find_next('td')
    stuff_overall = stuff_overall_td.text
    stuff_v_left_td = stuff_overall_td.find_next('td')
    stuff_v_left = stuff_v_left_td.text
    stuff_v_right_td = stuff_v_left_td.find_next('td')
    stuff_v_right = stuff_v_right_td.text
    stuff_potential_td = stuff_v_right_td.find_next('td')
    stuff_potential = stuff_potential_td.text
    pitcher_data.update({
        "stuff_ovr": stuff_overall,
        "stuff_vs_left": stuff_v_left,
        "stuff_vs_right": stuff_v_right,
        "stuff_pot": stuff_potential
    })
    pitching_ratings = soup.find('td', string='Movement')
    # print(pitching_ratings)
    skip1 = pitching_ratings.find_next('td')
    skip2 = skip1.find_next('td')
    movement_overall_td = skip2.find_next('td')
    movement_overall = movement_overall_td.text
    movement_v_left_td = movement_overall_td.find_next('td')
    movement_v_left = movement_v_left_td.text
    movement_v_right_td = movement_v_left_td.find_next('td')
    movement_v_right = movement_v_right_td.text
    movement_potential_td = movement_v_right_td.find_next('td')
    movement_potential = movement_potential_td.text
    pitcher_data.update({
        "movement_ovr": movement_overall,
        "movement_vs_left": movement_v_left,
        "movement_vs_right": movement_v_right,
        "movement_pot": movement_potential
    })

    pitching_ratings = soup.find('td', string='Control')
    skip1 = pitching_ratings.find_next('td')
    skip2 = skip1.find_next('td')
    control_overall_td = skip2.find_next('td')
    control_overall = control_overall_td.text
    control_v_left_td = control_overall_td.find_next('td')
    control_v_left = control_v_left_td.text
    control_v_right_td = control_v_left_td.find_next('td')
    control_v_right = control_v_right_td.text
    control_potential_td = control_v_right_td.find_next('td')
    control_potential = control_potential_td.text

    pitcher_data.update({
        "control_ovr": control_overall,
        "control_vs_left": control_v_left,
        "control_vs_right": control_v_right,
        "control_pot": control_potential
    })

    td_greg = soup.find_all('td')
    pitcher_label = 0
    pitcher_rating_loc = 0
    for d in td_greg:
        if d.text == 'Fastball':
            fastball_label = td_greg.index(d)
            fastball_current_rating = td_greg[fastball_label + 1].text
            fastball_pot_rating = td_greg[fastball_label + 2].text
            pitcher_data.update({
                "fastball_current": fastball_current_rating,
                "fastball_pot": fastball_pot_rating })
        if d.text == 'Curveball':
            curveball_label = td_greg.index(d)
            curveball_current_rating = td_greg[curveball_label + 1].text
            curveball_pot_rating = td_greg[curveball_label + 2].text
            pitcher_data.update({
                "curveball_current": curveball_current_rating,
                "curveball_pot": curveball_pot_rating})
        if d.text == 'Slider':
            slider_label = td_greg.index(d)
            slider_current_rating = td_greg[slider_label + 1].text
            slider_pot_rating = td_greg[slider_label + 2].text
            pitcher_data.update({
                "slider_current": slider_current_rating,
                "slider_pot": slider_pot_rating})
        if d.text == 'Forkball':
            forkball_label = td_greg.index(d)
            forkball_current_rating = td_greg[forkball_label + 1].text
            forkball_pot_rating = td_greg[forkball_label + 2].text
            pitcher_data.update({
                "forkball_current": forkball_current_rating,
                "forkball_pot": forkball_pot_rating})
        if d.text == 'Changeup':
            changeup_label = td_greg.index(d)
            changeup_current_rating = td_greg[changeup_label + 1].text
            changeup_pot_rating = td_greg[changeup_label + 2].text
            pitcher_data.update({
                "changeup_current": changeup_current_rating,
                "changeup_pot": changeup_pot_rating})
        if d.text == 'Cutter':
            cutter_label = td_greg.index(d)
            cutter_current_rating = td_greg[cutter_label + 1].text
            cutter_pot_rating = td_greg[cutter_label + 2].text
            pitcher_data.update({
                "cutter_current": cutter_current_rating,
                "cutter_pot": cutter_pot_rating})
        if d.text == 'Knuckleball':
            knuckleball_label = td_greg.index(d)
            knuckleball_current_rating = td_greg[knuckleball_label + 1].text
            knuckleball_pot_rating = td_greg[knuckleball_label + 2].text
            pitcher_data.update({
                "knuckleball_current": knuckleball_current_rating,
                "knuckleball_pot": knuckleball_pot_rating})
        if d.text == 'Sinker':
            sinker_label = td_greg.index(d)
            sinker_current_rating = td_greg[sinker_label + 1].text
            sinker_pot_rating = td_greg[sinker_label + 2].text
            pitcher_data.update({
                "sinker_current": sinker_current_rating,
                "sinker_pot": sinker_pot_rating})
        if d.text == 'Splitter':
            splitter_label = td_greg.index(d)
            splitter_current_rating = td_greg[splitter_label + 1].text
            splitter_pot_rating = td_greg[splitter_label + 2].text
            pitcher_data.update({
                "splitter_current": splitter_current_rating,
                "splitter_pot": splitter_pot_rating})
        if d.text == 'Knuckle Curve':
            knuckle_curve_label = td_greg.index(d)
            knuckle_curve_current_rating = td_greg[knuckle_curve_label + 1].text
            knuckle_curve_pot_rating = td_greg[knuckle_curve_label + 2].text
            pitcher_data.update({
                "knuckle_curve_current": knuckle_curve_current_rating,
                "knuckle_curve_pot": knuckle_curve_pot_rating})

    td_greg = soup.find_all('td')
    pitcher_label = 0
    pitcher_rating_loc = 0
    for d in td_greg:
        if d.text == 'Velocity':
            velocity_label = td_greg.index(d)
            break

    velocity_rating = td_greg[velocity_label + 1].text
    stamina_rating = td_greg[velocity_label + 3].text
    suggested_role = td_greg[velocity_label + 5].text
    type_rating = td_greg[velocity_label + 7].text
    hold_runners_rating = td_greg[velocity_label + 9].text
    defense_rating = td_greg[velocity_label + 11].text
    pitcher_data.update({
        "velocity_rating": velocity_rating,
        "stamina_rating": stamina_rating,
        "suggested_role": suggested_role,
        "type_rating": type_rating,
        "hold_runners_rating": hold_runners_rating,
        "defense_rating": defense_rating
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

    pitcher_data.update({
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
    pitcher_data.update({
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

    pitcher_data.update({
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

    return pitcher_data