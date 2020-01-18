import RPi.GPIO as GPIO
import w1thermsensor
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class relay:
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
    
    def __init__(self):
        for channel in self.relay:
            GPIO.setup(self.relay[channel]['pin'], GPIO.OUT)
            GPIO.output(self.relay[channel]['pin'], GPIO.HIGH)
            
    def set_state(self,CH,state):
        if state==1:
            GPIO.output(self.relay[CH]['pin'],GPIO.LOW)
            self.relay[CH]['state']=GPIO.LOW   
        else:
            GPIO.output(self.relay[CH]['pin'],GPIO.HIGH)
            self.relay[CH]['state']=GPIO.HIGH

    def read_state(self,CH):
        if self.relay[CH]['state'] == GPIO.HIGH:
            return 0
        else:
            return 1
        
    
        
                
x = relay()
x.set_state(2,1)
GPIO.setup(7, GPIO.OUT)
ena = GPIO.PWM(7,100)
GPIO.setup(8, GPIO.OUT)
enb = GPIO.PWM(8,100)

ena.start(100)
enb.start(100)

GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)


GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
def getTemp():
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    if temp is not None:
        temp = round(temp,1)
    return temp

while True:
    temp = getTemp()
    print(temp)
    time.sleep(0.1)

        
        

    
        

