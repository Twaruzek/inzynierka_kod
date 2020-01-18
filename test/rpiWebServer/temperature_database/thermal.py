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
sensor = w1thermsensor.W1ThermSensor()




GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)

GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)


ena = GPIO.PWM(17,100)
enb = GPIO.PWM(8,100)

ena.start(100)
enb.start(0)







dbname='sdb.db'
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
    curs.execute("INSERT INTO tmp VALUES(datetime('now'),(?));", (temp,))
    conn.commit()
    conn.close()

def convert_date(date_bytes):
    return mdates.strpdate2num('%Y-%m-%d %H:%M:%S')(date_bytes.decode('ascii'))
def wykres():
    graphArray=[]
    conn=lite.connect(dbname)
    curs=conn.cursor()
    for row in curs.execute("SELECT * FROM tmp"):
        startingInfo = str(row).replace('(','').replace('u\'','').replace("'","").replace(')','')
        splitInfo = startingInfo.split(',')
        graphArrayAppend = splitInfo[0]+','+splitInfo[1]
        graphArray.append(graphArrayAppend)
        datestamp, value = np.loadtxt(graphArray,delimiter=',', unpack=True,
                              converters={ 0: convert_date})    
    fig = plt.figure()
    rect = fig.patch
    ax1 = fig.add_subplot(1,1,1, facecolor='white')
    plt.plot_date(x=datestamp, y=value, fmt='b-', label = 'value', linewidth=2)
    plt.show()

#main
def main():
    while True:
        temp = getTemp()
        print(temp)
        logData(1/temp)
        time.sleep(0.1)
        #if temp>25.0 and temp<26:
        #    os.system('python model.py')
            #GPIO.cleanup()
#ex
main()