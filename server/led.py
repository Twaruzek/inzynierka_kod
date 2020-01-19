import time
import board
import neopixel
import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)




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
    
    def __init__(self, leds, rgb,state):
        self.leds = leds
        self.rgb = rgb
        self.state= state
    def turn_on(self):
        self.state=1
        for led in self.leds:
            pixels[led]=(self.rgb[0],self.rgb[1],self.rgb[2])
    def turn_off(self):
        self.state=0
        turn_off_value=[0,0,0]
        for led in self.leds:
            pixels[led]=(turn_off_value[0],turn_off_value[1],turn_off_value[2])
    def change_color(self,rgb):
        self.state=1
        self.rgb=rgb
        for led in self.leds:
            pixels[led]=(self.rgb[0],self.rgb[1],self.rgb[2])
    def change_color_string(self,rgb_string):
        try:
            rgb = rgb_string.split(',')
            if rgb[0][:4]=='rgba':
                rgb[0]=rgb[0][5:]
                del rgb[3]
            else :
                rgb[0]=rgb[0][4:]
                rgb[2]=rgb[2][:len(rgb[2])-1]
            for i in range(0, len(rgb)): 
                rgb[i] = int(rgb[i])
            self.change_color(rgb)
        except:
            self.change_color([0,0,0])
    def get_color(self):
        color = 'rgba('+str(self.rgb[0])+','+str(self.rgb[1])+','+str(self.rgb[2])+',1)'
        return color
    def get_state(self):
        return self.state   
    def __del__(self):
        self.turn_off()
        
rgb1=[255,0,0]  
kitchen = room(rooms['kitchen'], rgb1,1)
bathroom = room(rooms['bathroom'],rgb1,1)
hall = room(rooms['hall'],rgb1,1)
living_room = room(rooms['living_room'],rgb1,1)






