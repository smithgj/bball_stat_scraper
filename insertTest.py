import mysql.connector
import time
import datetime

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="bn7999hd",
    database="smitty"
)

mycursor = mydb.cursor()

sql = "INSERT INTO test2 (player_id, rating) VALUES (%s, %s)"
val = ("asdf", "75")
try:
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")

except:
  mydb.rollback()
  print("failed to insert record")
  log = "error.log"
  ts = time.time()
  sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
  with open(log, 'a') as logfile:
    logfile.write(sttime + "failed to insert record" + '\n')
