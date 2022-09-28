import pandas as pd
import mysql.connector
data = pd.read_csv ('./attendance.csv', encoding="utf-16-le", encoding_errors="ignore", sep="\t")
df = pd.DataFrame(data)


connection = mysql.connector.connect(host='localhost', database='hassandb', user='hassane', password='1202')


if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

mysql_create_table_query = '''CREATE TABLE attendance(
Meeting_Name TEXT(100),
Meeting_Start_Time TEXT(100),
Meeting_End_Time TEXT(100),
Name TEXT(100),
Attendee_Email TEXT(100),
Join_Time TEXT(100),
Leave_Time TEXT(100),
Attendance_Duration TEXT(100),
Connection_Type TEXT(100))'''

cursor = connection.cursor()

cursor.execute(mysql_create_table_query)

for row in df.itertuples():
	cursor.execute('''
		INSERT INTO attendance(Meeting_Name, Meeting_Start_Time, Meeting_End_Time, Name, Attendee_Email, Join_Time, Leave_Time, Attendance_Duration, Connection_Type)
		VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
		''',
		(row.Meeting_Name,
		row.Meeting_Start_Time,
		row.Meeting_End_Time,
		row.Name,
		row.Attendee_Email,
		row.Join_Time,
		row.Leave_Time,
		row.Attendance_Duration,
		row.Connection_Type))
connection.commit()


