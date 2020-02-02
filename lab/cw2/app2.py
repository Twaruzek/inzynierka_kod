from flask import Flask, render_template
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = Flask(__name__)
relay = {
       1  : {'pin' : 5, 'state' : GPIO.HIGH},
       2  : {'pin' : 6, 'state' : GPIO.HIGH},
       3 : {'pin' : 13, 'state' : GPIO.HIGH},
       4 : {'pin' : 16, 'state' : GPIO.HIGH},
       5 : {'pin' : 19, 'state' : GPIO.HIGH},
       6 : {'pin' : 20, 'state' : GPIO.HIGH},
       7 : {'pin' : 21, 'state' : GPIO.HIGH},
       8 : {'pin' : 26, 'state' : GPIO.HIGH}
       }

for channel in relay:
    GPIO.setup(relay[channel]['pin'], GPIO.OUT)
    GPIO.output(relay[channel]['pin'],GPIO.HIGH)
	
state=[0,0,0,0,0,0,0,0]

@app.route('/')
def index():
    return render_template('index.html', st=state) 


@app.route('/<channel>/<onoff>')
def on_off(channel,onoff):
    channel=int(channel)
    if onoff == "on":
        GPIO.output(relay[channel]['pin'],GPIO.LOW)
        state[channel]=1
    else:
        GPIO.output(relay[channel]['pin'],GPIO.HIGH)
        state[channel]=0
        
    return render_template('index.html', st=state) 

    

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
