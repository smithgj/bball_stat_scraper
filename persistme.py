import mysql.connector
import time
import datetime


def persist_player_data(player_dict, mydb, mycursor):

    nick_name = ''
    name = player_dict.get('player_name')
    names = name.split()
    if len(names) == 2:
        first_name = names[0]
        last_name = names[1]
    else:
        first_name = names[0]
        last_name = names[len(names) - 1]

        i = 1
        while (i + 2) <= len(names):
            nick_name = nick_name + ' ' + names[i]
            i = i + 1
    nick_name = nick_name.split()

    sql = (
            "INSERT INTO player (id, last_name, first_name, nick_name, team_id, age, bats, throws, morale, dob, height, weight, contract, salary))"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (player_dict.get('player_id'), player_dict.get('last_name'), player_dict.get('first_name'),
            player_dict.get(nick_name), player_dict.get(team_id), player_dict.get(age), player_dict.get(bats),
            player_dict.get(throws), player_dict.get(morale), player_dict.get(birthday), player_dict.get(height),
            player_dict.get(weight), player_dict.get(contract), player_dict.get(salary))

    try:
        mycursor.execute(sql, data)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    except Exception as e:
        mydb.rollback()
        log = "error.log"
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
        with open(log, 'a') as logfile:
            logfile.write(sttime + "failed to insert record" + '\n')
            logfile.write(sttime + str(e) + '\n')

