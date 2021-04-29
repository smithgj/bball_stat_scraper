import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="bn7999hd",
  database="smitty"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE testTable (text1 VARCHAR(255), text2 VARCHAR(255))")