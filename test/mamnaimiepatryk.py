import serial
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5,GPIO.LOW)
ser = serial.Serial('/dev/ttyUSB0', 9600)
def x(z):
    ser.close()
    ser.open()
    z=z
    ser.write(z)
    ser.flush()
    ser.close()
    
    


    
    
while True:
    time.sleep(10)
    xz=b"90"
    y=b"50"
    x(xz)
    time.sleep(10)

        #line = ser.readline().decode('utf-8').rstrip()
        #print(line)
