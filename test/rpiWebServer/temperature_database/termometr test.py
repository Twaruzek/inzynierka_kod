import w1thermsensor
import RPi.GPIO as GPIO
import sqlite3 as lite
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)


GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)


#PIO.setup(5, GPIO.OUT)
#GPIO.output(5, GPIO.LOW)

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)

dbname='sdb.db'
sampleFreq = 1



GPIO.setup(7, GPIO.OUT)
ena = GPIO.PWM(7,100)
GPIO.setup(8, GPIO.OUT)
enb = GPIO.PWM(8,100)

ena.start(0)
enb.start(100)

#GPIO.setup(15, GPIO.OUT)
#enzarowa = GPIO.PWM(15,100)

#enzarowa.start(100)

dbname='sdb.db'
sampleFreq = 1

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
    curs.execute("INSERT INTO tmp VALUES(datetime('now'),(?));", (temp,))
    conn.commit()
    conn.close()

def convert_date(date_bytes):
    return mdates.strpdate2num('%Y-%m-%d %H:%M:%S')(date_bytes.decode('ascii'))

def main():
    while True:
        temp = getTemp()
        #logData(temp)
        print(temp)
        time.sleep(0.1)
        #if temp>25.0 and temp<26:
        #    os.system('python model.py')
            #GPIO.cleanup()
#ex
main()