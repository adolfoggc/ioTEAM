#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------

import sqlite3

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="""


drop table if exists LIGHT ;
create table LIGHT (
  id integer primary key autoincrement,
  --SensorID text,
  Date_n_Time text,
  State text
);


drop table if exists PRESENCE ;
create table PRESENCE (
  id integer primary key autoincrement,
  --SensorID text,
  Date_n_Time text,
  Detection text
);

drop table if exists ACTION ;
create table ACTION (
  id integer primary key autoincrement,
  --SensorID text,
  Date_n_Time text,
  State text
);

"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
