import serial
import time
from controller import *
#from relay import *

serial=serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(0.2)
working=0



v=["99!","98!","97!","96!","95!","94!","93!","92!","91!","90!","89!","88!","87!","86!","85!","84!","83!","82!","81!","80!","79!","78!","77!","76!","75!","74!","73!","72!","71!","70!","69!","68!","67!","66!","65!","64!","63!","62!","61!","60!","59!","58!","57!","56!","55!","54!","53!","52!","51!","50!","49!","48!","47!","46!","45!","44!","43!","42!","41!","40!","39!","38!","37!","36!","35!","34!","33!","32!","31!","30!","29!","28!","27!","26!","25!","24!","23!","22!","21!","20!","19!","18!","17!","16!","15!","14!","13!","12!","11!","10!","9!","8!","7!","6!","5!","4!","3!","2!","2!","2!"]
d=[7,7,7,7,7,6,6,6,6,6,5,5,5,5,5,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2.5,2.5,2.5,2.5,2.5,2.25,2.25,2.25,2.25,2.25,2,2,2,2,2,1.85,1.85,1.85,1.85,1.85,1.75,1.75,1.75,1.75,1.75,1.6,1.6,1.6,1.6,1.6,1.5,1.5,1.5,1.5,1.5,1.35,1.35,1.35,1.35,1.35,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25]
    

def comunication(value,working):
    try:
        if value<0:
            value=99
        delay=d[value]
        value=v[value].encode('UTF-8')
        print("na arduino")
        print(value)
        if working == 0:
            print("po if")
            working =1
            serial.close()
            serial.open()
            serial.write(value)
            serial.flush()
            serial.close()
            time.sleep(delay)
            working=0
    except:
        pass
        
#controller_h=controller(1,"heat",0,0)
# controller_c=controller(1,"cool",0,0)
# relay_o.set_state(11,1)
# relay_o.set_state(12,1)
# relay_o.set_state(13,1)
# relay_o.set_state(14,1)
# relay_o.set_state(1,0)

while True:
    #controller_h.update()
    #comunication(int(controller_h.dim),working)
    controller_c.update()
    print("ena = " +str(controller_c.dim))
    
    