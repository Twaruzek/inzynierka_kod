import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)