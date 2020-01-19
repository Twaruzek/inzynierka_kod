import serial
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
ser = serial.Serial('/dev/ttyUSB1', 115200)
time.sleep(.2)
ser.close()
c=0
def x(z):
    ser.close()
    ser.open()
    z=z
    ser.write(z)
    ser.flush()
    ser.close()
    
    

def dobra(z,c,delay):
    if c==0:
        c=1
        
        ser.close()
        ser.open()
        z=z
        ser.write(z)
        ser.flush()
        ser.close()
        time.sleep(delay)
        c=0       
    
    
#while True:
    #xz=[90,80,70,60,50]
    #xk=bytearray(xz)
    #xz=[b"90",b"80",b"70",b"60",b"50"]
y=b"50"
    #for x in xz:
#x(b"70")

v=["9","8","7","6","5","4","3","2","1"]

time.sleep(1)
for i in range(10):
    w=v[i].encode('UTF-8')
    print(w)
    dobra(w,c,1.1)

#    time.sleep(1)

        #line = ser.readline().decode('utf-8').rstrip()
        #print(line)
