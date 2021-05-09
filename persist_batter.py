import mysql.connector
import time
import datetime


def persist_batter_data(player_dict, mydb, mycursor):

    sql = (
            "INSERT INTO batter_stats (player_id, contact_ovr, contact_pot, contact_vs_left, contact_vs_right, "
            "gap_ovr, gap_pot, gap_vs_left, gap_vs_right, power_ovr, power_pot, power_vs_left, power_vs_right, "
            "eye_ovr, eye_pot, eye_vs_left, eye_vs_right, avoidk_ovr, avoidk_pot, avoidk_vs_left, avoidk_vs_right, "
            "speed, stealing, baserunning, bunt_sac, bunt_hit)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (player_dict.get('player_id'), player_dict.get('contact_ovr'), player_dict.get('contact_pot'),
            player_dict.get('contact_vs_left'),
            player_dict.get('contact_vs_right'), player_dict.get('gap_ovr'), player_dict.get('gap_pot'),
            player_dict.get('gap_vs_left'), player_dict.get('gap_vs_right'), player_dict.get('pwr_ovr'),
            player_dict.get('pwr_pot'), player_dict.get('pwr_vs_left'), player_dict.get('pwr_vs_right'),
            player_dict.get('eye_ovr'), player_dict.get('eye_pot'), player_dict.get('eye_vs_left'),
            player_dict.get('eye_vs_right'), player_dict.get('avoidK_ovr'), player_dict.get('avoidK_pot'),
            player_dict.get('avoidK_vs_left'), player_dict.get('avoidK_vs_right'), player_dict.get('running_speed'),
            player_dict.get('stealing_ability'), player_dict.get('baserunning'), player_dict.get('sac_bunt'),
            player_dict.get('bunt_hit'))

    try:
        mycursor.execute(sql, data)
        mydb.commit()
        print(mycursor.rowcount, "table: batter_stats - record inserted.")

    except Exception as e:
        mydb.rollback()
        log = "error.log"
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
        with open(log, 'a') as logfile:
            logfile.write(sttime + "failed to insert record for " + player_dict.get('player_id') + '\n')
            logfile.write(sttime + str(e) + '\n')
