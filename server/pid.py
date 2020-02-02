
class PID:
    def __init__(self, P, I, D, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min
        self.set_point=0.0
        self.error=0.0
        self.Td=P/D
        self.Ti=P/I

    def update(self,current_value):
            
        self.error = self.set_point - current_value
        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki
                
        PID = self.P_value + self.I_value + self.D_value
        return PID

    def setPoint(self,set_point):
        self.set_point = set_point
        self.Integrator=0
        self.Derivator=0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ti=I
        self.Ki=(1/(self.Ti))*self.Kp

    def setKd(self,D):
        self.Td=D
        self.Kd=(1/(self.Td))*self.Kp

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator
	
    def reset(self,CH):
        if CH == "cooling":
            self.Kp=10.21
            self.Ki=10.21/254
            self.Kd=10.21/63.5
            self.Ti=254
            self.Td=63.5
        if CH == "heating":
            self.Kp=4.37
            self.Ki=4.37/590
            self.Kd=4.37/147.5
            self.Ti=590
            self.Td=147.5
		
	    

pid_h=PID(4.37,4.37/590,4.37/147.5, Integrator_max=100, Integrator_min=0)
pid_h.setPoint(30.0)
pid_c=PID(10.21,10.21/254,10.21/63.5, Integrator_max=100, Integrator_min=0)
pid_c.setPoint(20.0)
