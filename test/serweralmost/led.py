import time
import board
import neopixel
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)


pixel_pin = board.D18
num_pixels = 37
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3) 




rooms = {
    'hall'        : [0,1,15,16,17,18],
    'living_room' : [2,3,4,12,13,14,19,20,21,29,30,31,32,33,34],
    'kitchen'     : [5,6,7,8,9,10,11,22,23,24,25,26],
    'bathroom'    : [27,28,35,36]
    }

class room():
    def __init__(self, leds, rgb):
        self.leds = leds
        self.rgb = rgb
    def turn_on(self):
        for led in self.leds:
            pixels[led]=(self.rgb[0],self.rgb[1],self.rgb[2])
    def turn_off(self):
        turn_off_value=[0,0,0]
        for led in self.leds:
            pixels[led]=(turn_off_value[0],turn_off_value[1],turn_off_value[2])
    def change_color(self,rgb):
        self.rgb=rgb
        for led in self.leds:
            pixels[led]=(self.rgb[0],self.rgb[1],self.rgb[2])
    def __del__(self):
        self.turn_off()
        
    
            
    



    




while True:
    rgb1=[255,0,0]
    rgb2=[0,255,0]
    rgb3=[0,0,255]
    rgb4=[255,255,0]
    kitchen = room(rooms['kitchen'], rgb1)
    bathroom = room(rooms['bathroom'],rgb2)
    hall = room(rooms['hall'],rgb3)
    living_room = room(rooms['living_room'],rgb4)
    bathroom.turn_on()
    kitchen.turn_on()
    hall.turn_on()
    living_room.turn_on()
    rgb2=[0,255,255]
    




    
    time.sleep(10)


    
    #cooling(0,96,255)