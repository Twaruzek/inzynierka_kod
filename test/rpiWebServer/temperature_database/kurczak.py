
import RPi.GPIO as GPIO  
import time
from time import sleep
import sys  # this lets us have a time delay (see line 12)  
  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(14, GPIO.IN)    # set GPIO25 as input (button)  
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)    
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel,dim): # if port 25 == 1  
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
 
GPIO.add_event_detect(14, GPIO.RISING, callback=my_callback(50)) 
        
        


