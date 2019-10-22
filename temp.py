import w1thermsensor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
sensor = w1thermsensor.W1ThermSensor()




GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)

GPIO.setup(23, GPIO.OUT)
ena = GPIO.PWM(23,50)
GPIO.setup(24, GPIO.OUT)
enb = GPIO.PWM(24,50)

ena.start(100)
enb.start(100)

GPIO.setup(5,GPIO.OUT)
GPIO.output(5,GPIO.LOW)

while True:
    temp = sensor.get_temperature()
    print(temp)

