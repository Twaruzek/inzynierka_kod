import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sqlite3 as lite
import time
import datetime

def convert_date(date_bytes):
    return mdates.strpdate2num('%Y-%m-%d %H:%M:%S')(date_bytes.decode('ascii'))

dbname='sdb_grzanie.db'

conn=lite.connect(dbname)
curs=conn.cursor()
# Data for plotting

graphArray=[]

for row in curs.execute("SELECT * FROM tmp ORDER By time DESC LIMIT 2105"):
    startingInfo = str(row).replace('(','').replace('u\'','').replace("'","").replace(')','')
    splitInfo = startingInfo.split(',')
    graphArrayAppend = splitInfo[0]+','+splitInfo[1]
    graphArray.append(graphArrayAppend)
datestamp, value = np.loadtxt(graphArray,delimiter=',', unpack=True,
                              converters={ 0: convert_date})    
value=list(reversed(value))    
fig = plt.figure()

rect = fig.patch
t=np.arange(0,4210,2)
ax1 = fig.add_subplot(1,1,1, facecolor='white')
plt.plot(t, value)
plt.grid(b=None, which='major', axis='both')

minX=min(t)
maxX=max(t)

stable_value=80
p=np.polyfit(t,value,16)
deriv = np.polyder(p)
pointVal = 480.0
y_value_at_point = np.polyval(p, pointVal)
slope_at_point = np.polyval(deriv, pointVal)
ylow=(minX-pointVal)*slope_at_point + y_value_at_point
yhigh=(maxX-pointVal)*slope_at_point + y_value_at_point
plt.plot([minX,maxX],[ylow,yhigh],color='black')
plt.hlines(stable_value,0,5400,colors='r',linestyles='dashed')
t_horizontal=(stable_value-y_value_at_point+slope_at_point*pointVal)/slope_at_point
t0_horizontal=(min(value)-y_value_at_point+slope_at_point*pointVal)/slope_at_point
plt.vlines(t_horizontal,0,(stable_value+10),colors='r',linestyles='dashed')
plt.vlines(t0_horizontal,0,(min(value)+15),colors='r',linestyles='dashed')
plt.text(t_horizontal+50,20,'T₂='+str(int(t_horizontal))+'s')
plt.text(t0_horizontal+50,20,'T₁='+str(int(t0_horizontal))+'s')
plt.axis([-5,4210,15,85])
ax1.set_ylabel('Temperatura [°C]')
ax1.set_xlabel('Czas [s]')


'''
p=np.polyfit(t,value,16)
plt.plot(t,np.polyval(p,t))
#x= np.linspace(0,3002,1501)
#print(np.polyfit(x,np.log(value),1))
'''
#plt.figure()
#t = np.linspace(0,1600,100)
#y = 16.3 + 17.5*np.exp(-t/777)
#plt.grid(b=None, which='major', axis='both')
#plt.plot(t,y)

plt.show()
    