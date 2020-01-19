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
        
relay_o=relay()
        


        

        
    
        


        
        

    
        

