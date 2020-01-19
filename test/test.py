import serial
import RPi.GPIO as GPIO
import struct
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(5, GPIO.OUT)
GPIO.output(5,GPIO.LOW)

arduino = serial.Serial('/dev/ttyUSB1', 9600)


x="9"
y=bytes(x,'utf-8')
arduino.write('hello'.encode("utf-8"))
s=arduino.readline()
s=s.strip()
print(s.decode("utf-8"))