import RPi.GPIO as GPIO
import time
import httplib, urllib
import mysql.connector
import datetime
import config

updateDbTimer = 0
currentStreak = 0

valuesOnMinute = [0] * 60
ignoreCount = 0

minuteCounter = 60

#Setup Mysql settings
mydb = mysql.connector.connect(
  host=config.dbHost,
  user=config.dbUser,
  password=config.dbPassword,
  database=config.dbDatabase
)

GPIO.setmode(GPIO.BCM)

#Set pins
GPIO_TRIGGER = 14
GPIO_ECHO = 15

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#Calculate distance in cm
def distance():
	GPIO.output(GPIO_TRIGGER, True)

	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()
	
	
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()

	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	TimeElapsed = StopTime - StartTime

	distance = (TimeElapsed * 34300) / 2

	return 160 - distance

#Send notification to phone
def sendNotification(dist):
	conn = httplib.HTTPSConnection("pushsafer.com:443")
	conn.request("POST", "/api",
		urllib.urlencode({
			"k": config.notSecret,
			"m": "%.1f cm" % dist,
			"t": "Lunta",
			"i": "63",
			"s": "3",
			"v": "",
			"p": "",
		}), { "Content-type": "application/x-www-form-urlencoded" })
	response = conn.getresponse()

	print (response.status, response.reason)
	data = response.read()
	print (data)

#Update values to database
def updateDatabase(lumiMaara):
	global minuteCounter
	mycursor = mydb.cursor()

	sql = "UPDATE lumi SET lumimaara = '%s' WHERE paikka = 'koti'"
	data = (lumiMaara,)
	mycursor.execute(sql, data)

	mydb.commit()
	print(mycursor.rowcount, "record(s) affected") 
	print(minuteCounter)

	if(minuteCounter >= 60):
		minuteCounter = 0
		print(minuteCounter)
		now = datetime.datetime.now()
		sql2 = "INSERT INTO historia (date, lumimaara) VALUES (%s, %s)"
		data2 = (now, lumiMaara)
		mycursor.execute(sql2, data2)

		mydb.commit()
		print(mycursor.rowcount, "record(s) affected") 


#Get median value of distances over one minute
def getMedianOfValues(ignoreCount):
	valuesOnMinute.sort()
	ignoreCount = int(ignoreCount / 2)
	medianValue = valuesOnMinute[30 - ignoreCount]
	return medianValue


#Main loop
if __name__ == '__main__':
	try:
		while True:
			dist = distance()
			print ("Measured Distance = %.1f cm" % dist)
			valuesOnMinute[updateDbTimer] = dist

			if dist > 1000:
				ignoreCount += 1		

			if(updateDbTimer >= 59):
				updateDbTimer = 0
				minuteCounter += 1
				medianValue = getMedianOfValues(ignoreCount)
				ignoreCount = 0
				updateDatabase(medianValue * 10)

				#If amount of snow is greater than x
				if medianValue > 15:				
					currentStreak += 1			
					#If amount of snow have stayed over x for 5 minutes	straight
					if currentStreak >= 5:
						currentStreak = 0
						sendNotification(medianValue)
				else:
					currentStreak = 0

			updateDbTimer += 1
			time.sleep(1)

	except KeyboardInterrupt:
		print ("Measurement stopped by User")
		GPIO.cleanup()
