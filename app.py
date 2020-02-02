from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from relay import relay
from views import *
import temperature
from relay import relay_o
from flask_colorpicker import colorpicker
from sys import path
from os import getcwd, name
import threading
import datetime
import serial

#######################
### PID, controller ###
#######################

from pwm import cooling, heating 
from pid import pid_h, pid_c
from controller import controller_h, controller_c



############################
### Serial communication ###
############################

serial=serial.Serial('/dev/ttyUSB0', 115200)

def to_arduino():
    working=0
    v=["99!","98!","97!","96!","95!","94!","93!","92!","91!","90!","89!","88!","87!","86!","85!","84!","83!","82!","81!","80!","79!","78!","77!","76!","75!","74!","73!","72!","71!","70!","69!","68!","67!","66!","65!","64!","63!","62!","61!","60!","59!","58!","57!","56!","55!","54!","53!","52!","51!","50!","49!","48!","47!","46!","45!","44!","43!","42!","41!","40!","39!","38!","37!","36!","35!","34!","33!","32!","31!","30!","29!","28!","27!","26!","25!","24!","23!","22!","21!","20!","19!","18!","17!","16!","15!","14!","13!","12!","11!","10!","9!","8!","7!","6!","5!","4!","3!","2!","2!","2!"]
    d=[7,7,7,7,7,6,6,6,6,6,5,5,5,5,5,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2.5,2.5,2.5,2.5,2.5,2.25,2.25,2.25,2.25,2.25,2,2,2,2,2,1.85,1.85,1.85,1.85,1.85,1.75,1.75,1.75,1.75,1.75,1.6,1.6,1.6,1.6,1.6,1.5,1.5,1.5,1.5,1.5,1.35,1.35,1.35,1.35,1.35,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25]
    while True:
        if controller_h.state==1:
            try:
                controller_h.update()
                value = int(controller_h.dim)
                if value<0:
                    value=99
                delay=d[value]
                value=v[value].encode('UTF-8')
                print("Value send to arduino = "+str(value))
                if working == 0:
                    working =1
                    serial.close()
                    serial.open()
                    serial.write(value)
                    serial.flush()
                    serial.close()
                    time.sleep(delay)
                    working=0
            except:
                pass
            
arduino=threading.Thread(target=to_arduino)
arduino.start()

####################################
### Peltier + Fan  communication ###
####################################

def to_controller():
    while True:
        if controller_c.state==1:
            try:
                controller_c.update()
                print("NO CHŁODZE            "+ str(controller_c.dim))
                relay_o.set_pwm("ena",controller_c.dim)
            except:
                pass
                
eng_controller=threading.Thread(target=to_controller)
eng_controller.start()
                


splitter = '\\' if name == 'nt' else '/'
path.append(
    splitter.join(
        getcwd().split(
            splitter
        )[:-1]
    )
)

app = Flask(__name__)

################
### Database ###
################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY']='nQ{j65rLbt|3#*~fEmwRQ&5HbHNXHK'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class temperature_all(db.Model):
    time = db.Column(db.String, primary_key=True)
    temperature = db.Column(db.Float)
    
def add_record():

    while True:
        record_x = temperature_all(time= datetime.datetime.now(),temperature=temperature.read_temp())
        db.session.add(record_x)
        db.session.commit()
        del record_x
        time.sleep(0.5)

#rec=threading.Thread(target=add_record)
#rec.start()
##################
### Blueprints ###
#################@

app.register_blueprint(main)
app.register_blueprint(control, url_prefix="/control")
app.register_blueprint(anakysis, url_prefix="/anakysis")
app.register_blueprint(project, url_prefix="/project")
app.register_blueprint(parameters, url_prefix="/parameters")
app.register_blueprint(database, url_prefix="/database")



GPIO.setwarnings(False)
colorpicker(app, local=['static/spectrum.js', 'static/spectrum.css'])






	
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    
		
