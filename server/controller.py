from pid import *
from pwm import *
from relay import *
from temperature import *


heating.start(0)

pid_h=PID(4.39,1/590,1/147.5, Integrator_max=100, Integrator_min=0)
pid_h.setPoint(50)




class controller():
    def __init__(self,state,device,mode,dim):
        self.state=state
        self.device=device
        self.mode=mode
        self.dim=dim
    
    def turn_on(self):
        self.state=1
        if self.device=="heat":
            relay.set_state(1,1)
    
    def turn_off(self):
        self.state=0
        if self.device=="heat":
            relay.set_state(1,0)
    
    def update(self):
        if self.state==1 and self.mode ==0:
            if self.device=="heat":
                print(read_temp())
                delta_temp=(pid_h.update(read_temp()))
                heating.changeDutyCycle(heating.calculateDutyCycle(delta_temp))
                self.dim=heating.dutyCycle
                print("+++++++++++++++++++++")
                print(self.dim)
                print("----------------------")
    def read_dim(self):
        return self.dim

                  
                

