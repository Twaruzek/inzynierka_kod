import sqlite3 as lite
import sys
import w1thermsensor
 
sensor = w1thermsensor.W1ThermSensor()
import time

dbname='tempdata.db'
sampleFreq = 1

#data from sensor
def getTemp():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    if temp is not None:
        temp = round(temp,1)
    return temp

#log data
def logData(temp):
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO TMP_data VALUES(datetime('now'),(?));", (temp,))
    conn.commit()
    conn.close()
    
#main
def main():
    while True:
        temp = getTemp()
        logData(temp)
        time.sleep(0.1)
#ex
main()

        


    

    