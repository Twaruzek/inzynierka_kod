import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


GPIO.setup(14,GPIO.IN)
GPIO.setup(15,GPIO.OUT)

GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)

dim=20

def plox(cznel):
    dt = 75*dim
    time.sleep(dt/1000000.0)
    GPIO.output(15, GPIO.HIGH)
    time.sleep(10/1000000.0)
    GPIO.output(15, GPIO.LOW)
    print('lel')
    

GPIO.add_event_detect(14, GPIO.RISING, callback=plox)




