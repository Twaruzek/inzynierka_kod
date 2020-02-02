from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import board
import neopixel
import time 
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


pixel_pin = board.D18
num_pixels = 37
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.4) 
	
state=[0,0,0,0,0,0,0,0]
rgb=[255,255,0]

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST' and 'R' in request.form:
        rgb[0] = int(request.form['R'])
    if request.method == 'POST' and 'G' in request.form:
        rgb[1] = int(request.form['G'])
    if request.method == 'POST' and 'B' in request.form:
        rgb[2] = int(request.form['B'])
        
    pixels[13]=(rgb[0],rgb[1],rgb[2])
    return render_template('index.html', st=state, rgbx=rgb) 


@app.route('/<channel>/<onoff>')
def on_off(channel,onoff):
    channel=int(channel)
    if onoff == "on":
        GPIO.output(relay[channel]['pin'],GPIO.LOW)
        state[channel]=1
    else:
        GPIO.output(relay[channel]['pin'],GPIO.HIGH)
        state[channel]=0
        

    time.sleep(0.2)
    pixels[13]=(rgb[0],rgb[1],rgb[2])
    return render_template('index.html', st=state, rgbx=rgb) 

    

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
