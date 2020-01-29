from pid import *
from pwm import cooling, heating
from temperature import *



class controller():
    def __init__(self,state,device,mode,dim):
        self.state=state
        self.device=device
        self.mode=mode
        self.dim=dim
    
    def turn_on(self):
        self.state=1
            
    def turn_off(self):
        self.state=0
  
    def update(self):
        if self.state==1 and self.mode ==0:
            if self.device=="heat":
                print("Temperatura = "+str(read_temp()))
                delta_temp=(pid_h.update(read_temp()))
                heating.changeDutyCycle(heating.calculateDutyCycle(delta_temp))
                self.dim=heating.dutyCycle
                print("DIM heat = "+str(self.dim))
            if self.device=="cool":
                print("temperatura = "+str(read_temp()))
                delta_temp=(pid_c.update(read_temp()))
                cooling.changeDutyCycle(cooling.calculateDutyCycle(delta_temp))
                self.dim=cooling.dutyCycle
                print("DIM cool = "+str(self.dim))
                
    def read_dim(self):
        return self.dim
    
    def get_state(self):
        return self.state()

                  
controller_h=controller(0,"heat",0,0)
controller_c=controller(0,"cool",0,0)                

