import mysql.connector
import time
import datetime


def persist_pitcher_data(player_dict, mydb, mycursor):

    sql = (
            "INSERT INTO pitching_stats (player_id, stuff_ovr, stuff_pot, stuff_vs_left, stuff_vs_right, "
            "movement_ovr, movement_pot, movement_vs_left, movement_vs_right, control_ovr, control_pot,"
            "control_vs_left, control_vs_right, fastball_cur, fastball_pot, curveball_cur, curveball_pot,"
            "changeup_cur, changeup_pot, cutter_cur, cutter_pot, splitter_cur, splitter_pot, sinker_cur,"
            "sinker_pot, knuckle_crv_cur, knuckle_crv_pot, knuckle_cur, knuckle_pot, forkball_cur, forkball_pot,"
            "slider_cur,slider_pot,velocity,stamina,suggested_role,type,hold_runners,defense,"
            "running_speed,stealing_ability,baserunning,bunt_sac,bunt_hit,"
            "pitch_rating_1,pitch_rating_2,pitch_rating_3,pitch_rating_4)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

        
    data = (player_dict.get('player_id'), player_dict.get('stuff_ovr'), player_dict.get('stuff_pot'),
            player_dict.get('stuff_vs_left'),
            player_dict.get('stuff_vs_right'), player_dict.get('movement_ovr'), player_dict.get('movement_pot'),
            player_dict.get('movement_vs_left'), player_dict.get('movement_vs_right'), player_dict.get('control_ovr'),
            player_dict.get('control_pot'), player_dict.get('control_vs_left'), player_dict.get('control_vs_right'),
            player_dict.get('fastball_current'), player_dict.get('fastball_pot'), player_dict.get('curveball_current'), player_dict.get('curveball_pot'),
            player_dict.get('changeup_current'), player_dict.get('changeup_pot'), player_dict.get('cutter_current'),
            player_dict.get('cutter_pot'),
            player_dict.get('splitter_current'), player_dict.get('splitter_pot'), player_dict.get('sinker_current'),
            player_dict.get('sinker_pot'),
            player_dict.get('knuckle_crv_current'), player_dict.get('knuckle_crv_pot'), player_dict.get('knuckle_current'),
            player_dict.get('knuckle_pot'),
            player_dict.get('forkball_current'), player_dict.get('forkball_pot'), player_dict.get('slider_current'),
            player_dict.get('slider_pot'),
            player_dict.get('velocity_rating'), player_dict.get('stamina_rating'), player_dict.get('suggested_role'),
            player_dict.get('type_rating'),
            player_dict.get('hold_runners_rating'), player_dict.get('defense_rating'), player_dict.get('running_speed'),
            player_dict.get('stealing_ability'),
            player_dict.get('baserunning'), player_dict.get('sac_bunt'), player_dict.get('bunt_hit'),
            player_dict.get('pitch_rating_1'), player_dict.get('pitch_rating_2'), player_dict.get('pitch_rating_3'),
            player_dict.get('pitch_rating_4'))


    try:
        mycursor.execute(sql, data)
        mydb.commit()
        print(mycursor.rowcount, "table: pitcher_stats - record inserted.")

    except Exception as e:
        mydb.rollback()
        log = "error.log"
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
        with open(log, 'a') as logfile:
            logfile.write(sttime + "failed to insert record for " + player_dict.get('player_id') + '\n')
            logfile.write(sttime + str(e) + '\n')
