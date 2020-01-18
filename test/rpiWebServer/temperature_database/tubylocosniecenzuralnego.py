from scipy.optimize import curve_fit
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sqlite3 as lite
import time
import datetime

def func(x, a, b, c):
    return a * np.exp(-b * x) + c


def convert_date(date_bytes):
    return mdates.strpdate2num('%Y-%m-%d %H:%M:%S')(date_bytes.decode('ascii'))

dbname='tempdata.db'

conn=lite.connect(dbname)
curs=conn.cursor()
# Data for plotting

graphArray=[]

for row in curs.execute("SELECT * FROM TMP_data"):
    startingInfo = str(row).replace('(','').replace('u\'','').replace("'","").replace(')','')
    splitInfo = startingInfo.split(',')
    graphArrayAppend = splitInfo[0]+','+splitInfo[1]+','+splitInfo[2]
    graphArray.append(graphArrayAppend)
datestamp, value, duration = np.loadtxt(graphArray,delimiter=',', unpack=True,
                              converters={ 0: convert_date})    
    
fig = plt.figure()

rect = fig.patch

ax1 = fig.add_subplot(1,1,1, facecolor='white')
plt.plot_date(x=datestamp, y=value, fmt='b-', label = 'value', linewidth=2)
plt.grid(b=None, which='major', axis='both')

x= np.linspace(0,3002,1501)


plt.figure()
t = np.linspace(0,1600,100)
y = 16.3 + 17.5*np.exp(-t/777)
plt.grid(b=None, which='major', axis='both')
#plt.plot(t,y)

#plt.show()
popt, pocv= curve_fit(func, duration, value)
print(popt)
plt.plot(duration, func(duration,*popt),'b-')
plt.plot(duration,value,'r')
plt.show();