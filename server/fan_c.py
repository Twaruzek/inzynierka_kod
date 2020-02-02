class fan_control():
    def __init__(self,state, pwm):
        self.state=state
        self.pwm=pwm
        
    def set_state(self,x):
        if x == 1:
            self.state=1
        if x == 0:
            self.state=0
            
    def set_pwm(self,x):
        self.pwm=x
            
    
fan_c=fan_control(0,0)