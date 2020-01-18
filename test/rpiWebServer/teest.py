
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(15, GPIO.OUT)    
x=GPIO.PWM(15, 50)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
x.start(50)
