#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------


import json
import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Temperature to DB Table
def Presence_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	#SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	Detection = json_Dict['Detection']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record('insert into PRESENCE (Date_n_Time, Detection) values (?,?)',[Data_and_Time, Detection])
	del dbObj
	print ('Inserted Presence Data into Database.')
	print ('')


def Light_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	#SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	State = json_Dict['State']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record('insert into LIGHT (Date_n_Time, State) values (?,?)',[Data_and_Time, State])
	del dbObj
	print ('Inserted Light Data into Database.')
	print ('')
	
def Action_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	#SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	State = json_Dict['State']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record('insert into ACTION (Date_n_Time, State) values (?,?)',[Data_and_Time, State])
	del dbObj
	print ('Inserted Action Data into Database.')
	print ('')


#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
	if Topic == 'IoTEAM/presence':
		Presence_Handler(jsonData)
	elif Topic == 'IoTEAM/light':
		Light_Handler(jsonData)
	elif Topic == 'IoTEAM/action':
		Action_Handler(jsonData)

#===============================================================
