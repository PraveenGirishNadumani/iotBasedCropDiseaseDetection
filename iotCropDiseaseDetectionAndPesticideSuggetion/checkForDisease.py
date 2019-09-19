import MySQLdb
import datetime
import mail

month = datetime.datetime.now().strftime("%m")

colorR=0
colorG=0
colorB=0
avgTemp=0;
avgHumidity=0
diseaseResult="Nothing"
diseasechanceAnthracnose=0
diseasechanceScoty=0
diseasechancePowdery=0
diseasechanceDieBack=0
diseasechancePhoma=0
diseasechanceBacterial=0
diseasechanceRedRust=0
colorResult="nothing"
humidityResult=0
temperatureResult=0
temp=0
def checkForColor():
	global colorR,colorG,colorB,colorResult,temp
	print "checking for color"
	colorResult="white"
	while temp<5:
		colorResult="red"
		temp++;
	if colorR<=480 and colorR>=200 and colorG>=600 and colorG<=670 and colorB>=770 and colorB<=870:
		colorResult="yellow"
	elif colorR>=920 and colorR<=990 and colorG>=1080 and colorG<=1150 and colorB>=1080 and colorB<=1150:
		colorResult="green"		
	elif colorR>=300 and colorR<=360 and colorG>=300 and colorG<=390 and colorB>=250 and colorB<=350:
		colorResult="white"
	elif colorR>=420 and colorR<=500 and colorG>=600 and colorG<=700 and colorB>=500 and colorB<=600:
		colorResult="black"
	elif colorR>=450 and colorR<=580 and colorG>=800 and colorG<=900 and colorB>=650 and colorB<=750:
		colorResult="brown"
	elif colorR>=200 and colorR<=300 and colorG>=350 and colorG<=550 and colorB>=630 and colorB<=330:
			colorResult="red" 
	print colorResult
def checkdiseasevalue():
		print"checking for disease"
		global diseasechanceAnthracnose,diseasechanceScoty,diseasechancePowdery,diseasechanceDieBack,diseasechancePhoma,diseasechanceBacterial,diseasechanceRedRust
		if diseasechanceAnthracnose>50 :
			print "anthracnose disease is Detected"
			print diseasechanceAnthracnose
			mail.send(1,"anthracnose disease Detected",str(diseasechanceAnthracnose))
		elif diseasechanceScoty > 50:
			print " Scoty mould disease Detected"
			print diseasechanceScoty
			mail.send(2,"Scoty mould disease Detected",str(diseasechanceScoty))
		elif diseasechancePowdery > 50 :
			print "Powder Mildway disease Detected"
			print diseasechancePowdery
			mail.send(3,"Powder mildway disease Detected",str(diseasechancePowdery))
		elif diseasechanceDieBack > 50 :
			print "Die Back disease Detected"
			print diseasechanceDieBack
			mail.send(4,"Die Back disease Detected",str(diseasechanceDieBack))
		elif diseasechancePhoma > 50 :
			print " Phoma blight disease Detected"
			print diseasechancePhoma
			mail.send(5,"phoma blight disease Detected",str(diseasechancePhoma))
		elif diseasechanceBacterial > 50 : 
			print " Bacterial canker disease Detected"
			print diseasechanceBacterial
			mail.send(6,"Bacterial canker disease Detected",str(diseasechanceBacterial))
		elif diseasechanceRedRust > 50 :
			print "Red Rust disease Detected"
			print diseasechanceRedRust
			mail.send(7,"Red Rust Disease Detected",str(diseasechanceRedRust))
		else:
			print "status is normal"
			#mail.send(8,"status is normal")

def checkfordisease():
		# checking for color of the leaf
	global colorResult,diseasechanceAnthracnose,diseasechanceScoty,diseasechancePowdery,diseasechanceDieBack,diseasechanceBacterial,diseasechanceRedRust,temperatureResult,month
	if colorResult=="black" :
		diseasechanceAnthracnose=diseasechanceAnthracnose+30
		diseasechanceScoty +=30
	if colorResult=="white" :
		diseasechancePowdery +=50
	if colorResult=="brown" :
		diseasechanceDieBack +=30
		diseasechancePhoma +=30
	if colorResult=="yellow" :
		diseasechanceBacterial +=60
	if colorResult=="red" :
		diseasechanceRedRust =80
	if colorResult=="grey" :
		diseasechanceRedRust +=60
	# checking for the temperature of the tree
	print "checking for Temperature and Humidity"
	if temperatureResult<35 and temperatureResult>23 :
		diseasechanceAnthracnose +=30
	if temperatureResult<45 and temperatureResult>35 :
		diseasechanceScoty +=30
	#if temperatureResult<25 :
		diseasechancePowdery +=20
	
	#cheking for the months 
	if month in ("october","november") :
		diseasechanceDieBack +=40
	checkdiseasevalue()
		
		


def check():
	global colorR,colorG,colorB,colorResult,diseasechanceRedRust,avgTemp,avgHumidity,temp
	connection=MySQLdb.connect("localhost","root","root","IOT")
	cursorX=connection.cursor()
	statementX="SELECT * FROM agrdata ORDER BY id DESC LIMIT 1;"
	cursorX.execute(statementX)	
	avgResult=cursorX.fetchall()
	for row in avgResult:
		colorR=row[1]
		print row[1]
		colorG=row[2]
		print row[2]
		colorB=row[3]
		print row[3]
		avgTemp=row[4]
		avgHumidity=row[5]
	connection.commit()
	connection.close()
	checkForColor()
	checkfordisease()
	temp+=1
	
