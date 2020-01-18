from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
import RPi.GPIO as GPIO
import io

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor= '/sys/bus/w1/devices/28-011452cc30aa/w1_slave'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY']='nQ{j65rLbt|3#*~fEmwRQ&5HbHNXHK'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
	
	
active=["","","","","","","","","",""]

relay = {
   5  : {'name' : 'Relay CH0', 'state' : GPIO.HIGH},
   6  : {'name' : 'Relay CH1', 'state' : GPIO.HIGH},
   13 : {'name' : 'Relay CH2', 'state' : GPIO.HIGH},
   16 : {'name' : 'Relay CH3', 'state' : GPIO.HIGH},
   19 : {'name' : 'Relay CH4', 'state' : GPIO.HIGH},
   20 : {'name' : 'Relay CH5', 'state' : GPIO.HIGH},
   21 : {'name' : 'Relay CH6', 'state' : GPIO.HIGH},
   28 : {'name' : 'Relay CH7', 'state' : GPIO.HIGH}
   }

class Log_Temp(db.Model):
	date = db.Column(db.DateTime, nullable = False, primary_key=True, default=datetime.utcnow)
	temp = db.Column(db.Float, nullable = False)
	
	def __repr__(self):
		return 'Logged temp ' +str(self.temp) + 'at ' + str(self.date)



# Ustawienie wszystkich pinow szyny przekaznikow
for pin in relay:
    GPIO.setup(pin, GPIO.OUT)  
    GPIO.output(pin, GPIO.HIGH)
    
# Odczyt temperatury
def get_raw_temp():
    f = open(sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = get_raw_temp()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = get_raw_temp()
    temp_output = lines[1].find('t=')
    if temp_output!=-1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
        return temp_c
        
def stateRead():
    for pin in relay:
        relay[pin]['state'] = GPIO.input(pin)
    return relay
        
def Active_Page(x):
	x=int(x)
	for i in range(10):
		if i == x :
			active[i] = "active"
		else:
			active[i] = ""
	return active 
	
 
	
@app.route('/')
def index():
	active_page=Active_Page(0)
	return render_template('index.html', active=active_page)
		
@app.route('/control')
def control():
	active_page=Active_Page(1)
	relayx = stateRead()
	templateData = {
        'relay' : relayx,
        'active': active_page
		}
	return render_template('control.html', **templateData)


@app.route('/control/<changePin>/<action>')
def action(changePin, action):
	active_page=Active_Page(1)
	changePin = int(changePin)
	deviceName = relay[changePin]['name']
	if action == "on":
		GPIO.output(changePin, GPIO.HIGH)
		message = "Turned " + deviceName + " on."
	if action == "off":
		GPIO.output(changePin, GPIO.LOW)
		message = "Turned " + deviceName + " off."
	relayx = stateRead()

	templateData = {
        'relay' : relayx,
        'active': active_page

   }
	return render_template('control.html', **templateData)
		
	
@app.route('/characteristic')
def characteristic():
	active_page=Active_Page(2)
	return render_template('characteristic.html', active=active_page)
	
@app.route('/reg')
def reg():
	active_page=Active_Page(3)
	return render_template('reg.html', active=active_page)
	
@app.route('/log')
def log():
	active_page=Active_Page(4)
	return render_template('log.html', active=active_page)
	
@app.route('/assumptions')
def assumptions():
	active_page=Active_Page(5)
	return render_template('assumptions.html', active=active_page)
	
@app.route('/authors')
def authors():
	active_page=Active_Page(6)
	return render_template('authors.html', active=active_page)
	
@app.route('/lab')
def lab():
	active_page=Active_Page(7)
	return render_template('lab.html', active=active_page)
	
@app.route('/eng')
def eng():
	active_page=Active_Page(8)
	return render_template('eng.html', active=active_page)
	
@app.route('/login')
def login():
	active_page=Active_Page(9)
	return render_template('login.html', active=active_page)	
	
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return 'wylogowano'

	

		
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
