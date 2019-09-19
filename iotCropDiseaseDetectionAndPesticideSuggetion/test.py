import requests
import json
import MySQLdb
import time
import checkForDisease

def agr():
	db=MySQLdb.connect("localhost","root","root","IOT")
	cursor1 = db.cursor()
	statement="CREATE TABLE IF NOT EXISTS agrdata(id INTEGER AUTO_INCREMENT PRIMARY KEY,colorR INTEGER,colorG INTEGER,colorB INTEGER, temperature INTEGER, humidity INTEGER);"
	cursor1.execute(statement)
	statement="select * from data ORDER BY id DESC LIMIT 3;"
	cursor1.execute(statement)
	agrResult=cursor1.fetchall()
	field1=0
	field2=0
	field3=0
	field4=0
	field5=0
	for row in agrResult:
		field1+=row[1]
		field2+=row[2]
		field3+=row[3]
		field4+=row[4]
		field5+=row[5]	
	field1=field1/3
	field2=field2/3
	field3=field3/3
	field4=field4/3
	field5=field5/3
	statement="INSERT INTO agrdata(colorR,colorG,colorB, temperature, humidity) VALUES(%s,%s,%s,%s,%s)"  
	#.format(field1,field2,field3,field4,field5)
	val=(field1,field2,field3,field4,field5)
	cursor1.execute(statement,val)	
	print "agr updated"
	db.commit()
	db.close()

#
#			the main progrma starts from here
#
count=0
while True:
	resp=requests.get("https://api.thingspeak.com/channels/767969/feeds.json?api_key=28CZZXUW761Q5A9K&results=2")
	x=resp.text
	final=x[x.find('['):-1]
	lists=json.loads(final)
	mydb = MySQLdb.connect("localhost","root","root","IOT")
	cursor = mydb.cursor()
	cursor.execute(" CREATE TABLE IF NOT EXISTS data (id INTEGER AUTO_INCREMENT PRIMARY KEY,colorR INTEGER, colorG INTEGER, colorB INTEGER, temperature INTEGER, humidity INTEGER);")
	for i in lists:
		print('Field 1: ',i['field1'])
		print('Field 2: ',i['field2'])
		print('Field 3: ',i['field3'])
		print('Field 4: ',i['field4'])
		print('Field 5: ',i['field5'])
		cursor.execute("INSERT INTO data(colorR, colorG, colorB,temperature,humidity) values ("+i['field1']+","+i['field2']+","+i['field3']+","+i['field4']+","+i['field5']+");")
	cursor.execute("select * from data;")
	z=cursor.fetchall()
	print(z)
	count+=1
	print count
	mydb.commit()
	mydb.close()
	if count>=3:
		agr()
		checkForDisease.check()
		count=0		
	time.sleep(3)

	





