import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sqlite3 as lite
import time
import datetime

def convert_date(date_bytes):
        return mdates.strpdate2num('%Y-%m-%d %H:%M:%S.%f')(date_bytes.decode('ascii'))


class data_log_graph():
    def __init__(self,max_g=40,min_g=10):
        self.max_g=max_g
        self.min_g=min_g
    def set_max(self,max_s):
        self.max_g=max_s
    
    def set_min(self,min_s):
        self.min_g=min_s
 

    
    def generate_graph(self, range_g):
 
        dbname='../db.db'
        conn=lite.connect(dbname)
        curs=conn.cursor()
        curs.execute('SELECT * FROM temperature_all').rowcount
        rows = curs.fetchall()
        if range_g>len(rows):
            range_g=len(rows)
            
        graphArray=[]
        conn=lite.connect(dbname)
        curs=conn.cursor()
        choose="SELECT * FROM temperature_all ORDER By time DESC LIMIT {}".format(str(range_g))
        for row in curs.execute(choose):
            startingInfo = str(row).replace('(','').replace('u\'','').replace("'","").replace(')','')
            splitInfo = startingInfo.split(',')
            graphArrayAppend = splitInfo[0]+','+splitInfo[1]
            graphArray.append(graphArrayAppend)
        conn.close()
        datestamp,value = np.loadtxt(graphArray,delimiter=',', unpack=True,converters={ 0: convert_date})
        value=list(value)
        
        
        fig = plt.figure()
        rect = fig.patch
        t=np.arange(0,range_g,1)
        ax1 = fig.add_subplot(1,1,1, facecolor='white')
        plt.plot(t,value)
        plt.grid(b=None, which='major', axis='both')
        ax1.set_ylabel('Temperatura [°C]')
        ax1.set_xlabel('Próbki')
        plt.axis([-5,range_g,self.min_g,self.max_g])
        output_dir = "static"
        fig.show()
        return fig
 
        

class parameters_graph():
    def __init__(self,max_g=40,min_g=10):
        self.max_g=max_g
        self.min_g=min_g
        self.inverted=0;
        self.point=100
    def set_max(self,max_s):
        self.max_g=max_s
    
    def set_min(self,min_s):
        self.min_g=min_s
 
    def invert(self,onoff):
        self.inverted=int(onoff)
        
    def set_point(self,point):
        self.point=point
    
    def generate_graph(self, range_g):
 
        dbname='../db.db'
        conn=lite.connect(dbname)
        curs=conn.cursor()
        curs.execute('SELECT * FROM temperature_all').rowcount
        rows = curs.fetchall()
        if range_g>len(rows):
            range_g=len(rows)
            
        graphArray=[]
        conn=lite.connect(dbname)
        curs=conn.cursor()
        choose="SELECT * FROM temperature_all ORDER By time DESC LIMIT {}".format(str(range_g))
        for row in curs.execute(choose):
            startingInfo = str(row).replace('(','').replace('u\'','').replace("'","").replace(')','')
            splitInfo = startingInfo.split(',')
            graphArrayAppend = splitInfo[0]+','+splitInfo[1]
            graphArray.append(graphArrayAppend)
        conn.close()
        datestamp,value = np.loadtxt(graphArray,delimiter=',', unpack=True,converters={ 0: convert_date})
        if self.inverted==1:
            value = list(reversed(value))
            value = np.reciprocal(value)
        else:
            value= list(reversed(value))
        
        fig = plt.figure()
        rect = fig.patch
        t = np.arange(0, range_g, 1)
        ax1 = fig.add_subplot(1, 1, 1, facecolor='white')
        plt.plot(t, value)
        plt.grid(b=None, which='major', axis='both')
        
        minX = min(t)
        maxX = max(t)
        
        stable_value = value[-1]
        p = np.polyfit(t, value, 10)
        deriv = np.polyder(p)
        pointVal = self.point
        y_value_at_point = np.polyval(p, pointVal)
        slope_at_point = np.polyval(deriv, pointVal)
        ylow = (minX - pointVal) * slope_at_point + y_value_at_point
        yhigh = (maxX - pointVal) * slope_at_point + y_value_at_point
        plt.plot([minX, maxX], [ylow, yhigh], color='black')
        plt.hlines(stable_value, 0, range_g, colors='r', linestyles='dashed')
        t_horizontal = (stable_value - y_value_at_point + slope_at_point * pointVal) / slope_at_point
        t0_horizontal = (min(value) - y_value_at_point + slope_at_point * pointVal) / slope_at_point
        plt.vlines(t_horizontal, 0, (stable_value + 10), colors='r', linestyles='dashed')
        plt.vlines(t0_horizontal, 0, (min(value) + 15), colors='r', linestyles='dashed')
        plt.text(t_horizontal + 50, 20, 'T₂=' + str(int(t_horizontal)) + 's')
        plt.text(t0_horizontal + 50, 20, 'T₁=' + str(int(t0_horizontal)) + 's')
        plt.axis([-5, range_g, self.min_g, self.max_g])
        ax1.set_ylabel('Temperatura [°C]')
        ax1.set_xlabel('Czas [s]')
        plt.show()
        
        
        return fig




# stable_value=0.0521
# p=np.polyfit(t,value,1)
# deriv = np.polyder(p)
# pointVal = 300.0
# y_value_at_point = np.polyval(p, pointVal)
# slope_at_point = np.polyval(deriv, pointVal)
# ylow=(minX-pointVal)*slope_at_point + y_value_at_point
# yhigh=(maxX-pointVal)*slope_at_point + y_value_at_point
# plt.plot([minX,maxX],[ylow,yhigh],color='black')
# plt.hlines(stable_value,0,5400,colors='r',linestyles='dashed')
# t_horizontal=(stable_value-y_value_at_point+slope_at_point*pointVal)/slope_at_point
# t0_horizontal=(min(value)-y_value_at_point+slope_at_point*pointVal)/slope_at_point
# plt.vlines(t_horizontal,0,(stable_value+10),colors='r',linestyles='dashed')
# plt.vlines(t0_horizontal,0,(min(value)+0.002),colors='r',linestyles='dashed')
# plt.text(t_horizontal+50,0.045,'T₂='+str(int(t_horizontal))+'s')
# plt.text(t0_horizontal+50,0.045,'T₁='+str(int(t0_horizontal))+'s')
# plt.axis([-5,3000,0.044,0.054])
# ax1.set_ylabel('1/Temperatura [1/°C]')
# ax1.set_xlabel('Czas [s]')



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


    
