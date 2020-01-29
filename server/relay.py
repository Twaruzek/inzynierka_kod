import RPi.GPIO as GPIO
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
       8 : {'pin' : 26, 'state' : GPIO.HIGH},
       9 : {'pin' : 15, 'state' : GPIO.LOW},
       10 : {'pin' : 8, 'state' : GPIO.LOW},
       11 : {'pin' : 9, 'state' : GPIO.LOW},
       12 : {'pin' : 10, 'state' : GPIO.LOW},
       13 : {'pin' : 11, 'state' : GPIO.LOW},
       14 : {'pin' : 12, 'state' : GPIO.LOW},
       15 : {'pin' : 18, 'state' : GPIO.LOW}      
       }
    GPIO.setup(15,GPIO.OUT)
    GPIO.setup(8,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    ena = GPIO.PWM(15,1000)
    enb = GPIO.PWM(8,10)
    ledpwm = GPIO.PWM(18,1000)

    ledpwm.start(0)


    
    def __init__(self):
        for channel in self.relay:
            GPIO.setup(self.relay[channel]['pin'], GPIO.OUT)
            GPIO.output(self.relay[channel]['pin'],GPIO.HIGH)
            
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
    
    def set_pwm(self,CH,PWM):
        if CH == "ena":
            print("PWM = "+str(PWM))
            self.ena.stop()
            self.ena.start(int(PWM))

            
            
        if CH == "enb":
            self.enb.ChangeDutyCycle(PWM)
        if CH == "ledpwm":
            self.ledpwm.ChangeDutyCycle(PWM)
            
            
relay_o=relay()


        

        
    
        


        
        

    
        

