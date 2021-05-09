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
    nick_name = nick_name.strip()
    bday = player_dict.get('birthday')
    dob = datetime.datetime.strptime(bday, "%m/%d/%Y").strftime("%Y-%m-%d")
    if player_dict.get('team_id') == '':
        team_id = '0'
    else:
        team_id = player_dict.get('team_id')

    weight_text = player_dict.get('weight').split()
    weight = weight_text[0]

    salary = player_dict.get('salary')
    if salary == '-':
        salary='0'
    if salary[0:1] == '$':
        salary = salary[1:]
    salary = salary.replace(',','')


    sql = (
            "INSERT INTO player (id, last_name, first_name, nick_name, team_id, age, bats, throws, morale, dob, height, weight, contract, salary)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (player_dict.get('player_id'), last_name, first_name, nick_name,
            team_id, player_dict.get('age'), player_dict.get('bats'),
            player_dict.get('throws'), player_dict.get('morale'), dob, player_dict.get('height'),
            weight, player_dict.get('contract'), salary)

    try:
        mycursor.execute(sql, data)
        mydb.commit()
        print(mycursor.rowcount, "table: player - record inserted.")

    except Exception as e:
        mydb.rollback()
        log = "error.log"
        ts = time.time()
        sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
        with open(log, 'a') as logfile:
            logfile.write(sttime + "failed to insert record" + '\n')
            logfile.write(sttime + str(e) + '\n')

