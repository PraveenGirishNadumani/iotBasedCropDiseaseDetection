# Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib 
import MySQLdb
 

def send(Did,diseaseName,chance):
 	connection=MySQLdb.connect("localhost","root","root","IOT")
	cursorX=connection.cursor()
	statementX="""SELECT pesticide FROM pesticideTable where id =%s;"""
	cursorX.execute(statementX,(Did, ))
	Presult=cursorX.fetchall()

	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
  
	# start TLS for security 
	s.starttls() 
  
	# Authentication 
	s.login("iotprojectacount@gmail.com", "raPking@123") 
  
	# message to be sent 
	msg = str(Presult[0])
  	message=diseaseName
	message+=","
	message+="\nChance of disease exist is "
	message+=chance
	message+="% \n"
	message+="To control the disease "
	message+=msg	
	print message	
	# sending the mail 
	s.sendmail("iotprojectacount@gmail.com", "iotprojectacount@gmail.com",message) 
  
	# terminating the session 
	s.quit() 
