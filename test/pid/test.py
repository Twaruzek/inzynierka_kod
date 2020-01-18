
import pid as pid,pwm_weather as pwm
from time import sleep
import RPi.GPIO as GPIO
import os
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
fan = pwm.pwm(60,7,4.39,5,0.2,"heat")
p = pid.PID(4.39,1/590,1/147.5, Integrator_max=100, Integrator_min=0)
p.setPoint(47.0)
#start fan @ 0 
fan.start(0)
dim=fan.dutyCycle
  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(14, GPIO.IN)    # set GPIO25 as input (button)  
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)    
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)
def my_callback(channel): # if port 25 == 1
        dim=fan.dutyCycle
        if dim > 70:
            dt = 75*dim
            start=1000000*time.time()
            stop=0
            while (stop-start)<dt:
                stop=1000000*time.time()
              
            GPIO.output(15, GPIO.HIGH)
            start2=1000000*time.time()
            stop2=0
            while (stop2-start2)<13:
                stop2=1000000*time.time()
            GPIO.output(15, GPIO.LOW)
            start=0
            start2=0
            stop2=0
            stop=0
        else:
            GPIO.output(15, GPIO.LOW)
 
GPIO.add_event_detect(14, GPIO.RISING, callback=my_callback) 

try:
 while True:
  sleep(.5)
  #get temperature from my pwm class and pass it into the pid loop update
  x = (p.update(pwm.temp()))*-1
  print('Temp: '+str(pwm.temp()))
  fan.changeDutyCycle(fan.calculateDutyCycle(x))
  dim=fan.dutyCycle
  print(dim)
except KeyboardInterrupt:
  fan.stop()
  pass
 