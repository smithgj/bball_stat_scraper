import mysql.connector
import time
import datetime


def convert_data(txtval):
    if txtval == '-':
        retval = 0
    else:
        retval = txtval
    return retval




def persist_fielding_data(player_dict, mydb, mycursor):
    catcher_range = convert_data(player_dict.get('catcher_range'))
    infield_range = convert_data(player_dict.get('infield_range'))
    outfield_range = convert_data(player_dict.get('outfield_range'))
    catcher_errors = convert_data(player_dict.get('catcher_errors'))
    infield_errors  = convert_data(player_dict.get('infield_errors'))
    outfield_errors  = convert_data(player_dict.get('outfield_errors'))
    catcher_arm  = convert_data(player_dict.get('catcher_arm'))
    infield_arm  = convert_data(player_dict.get('infield_arm'))
    outfield_arm  = convert_data(player_dict.get('outfield_arm'))
    catcher_turndp  = convert_data(player_dict.get('catcher_turndp'))
    infield_turndp  = convert_data(player_dict.get('infield_turndp'))
    outfield_turndp  = convert_data(player_dict.get('outfield_turndp'))
    catcher_ability  = convert_data(player_dict.get('catcher_ability'))
    infield_ability  = convert_data(player_dict.get('infield_ability'))
    outfield_ability  = convert_data(player_dict.get('outfield_ability'))
    pitcher_rating  = convert_data(player_dict.get('pitcher_rating'))
    catcher_rating  = convert_data(player_dict.get('catcher_rating'))
    firstbase_rating  = convert_data(player_dict.get('firstbase_rating'))
    secondbase_rating  = convert_data(player_dict.get('secondbase_rating'))
    thirdbase_rating  = convert_data(player_dict.get('thirdbase_rating'))
    ss_rating  = convert_data(player_dict.get('ss_rating'))
    lf_rating  = convert_data(player_dict.get('lf_rating'))
    cf_rating  = convert_data(player_dict.get('cf_rating'))
    rf_rating  = convert_data(player_dict.get('rf_rating'))

    sql = (
            "INSERT INTO fielding_stats (player_id, catcher_range, infield_range, outfield_range, catcher_errors, "
            "infield_errors, outfield_errors, catcher_arm, infield_arm, outfield_arm, catcher_turn2, infield_turn2, "
            "outfield_turn2, catcher_ability, infield_ability, outfield_ability, pitcher_rating, catcher_rating,  "
            "1b_rating, 2b_rating, 3b_rating, ss_rating, lf_rating, cf_rating, rf_rating)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s)"
    )
    data = (player_dict.get('player_id'), catcher_range, infield_range,
            outfield_range, catcher_errors, infield_errors, outfield_errors,
            catcher_arm, infield_arm, outfield_arm, catcher_turndp, infield_turndp, outfield_turndp,
            catcher_ability, infield_ability, outfield_ability, pitcher_rating, catcher_rating, firstbase_rating,
            secondbase_rating, thirdbase_rating, ss_rating, lf_rating, cf_rating, rf_rating)

    try:
        mycursor.execute(sql, data)
        mydb.commit()
        print(mycursor.rowcount, "table: fielding_stats - record inserted.")

    except Exception as e:
        mydb.rollback()
        log = "error.log"
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
        with open(log, 'a') as logfile:
            logfile.write(sttime + "failed to insert record for " + player_dict.get('player_id') + '\n')
            logfile.write(sttime + str(e) + '\n')
