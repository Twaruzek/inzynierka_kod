import time
import threading
import math

class pwm(threading.Thread):

    def __init__(self,frequency,break_point,hysteresis,device):
        
        self.break_point = break_point
        self.hysteresis = hysteresis
        self.device = device
        self.baseTime = 1.0 / frequency
        self.maxCycle = 100.0
        self.sliceTime = self.baseTime / self.maxCycle
        self.terminated = False
        self.toTerminate = False


    def start(self, dutyCycle):
        
        self.dutyCycle = dutyCycle
        self.thread = threading.Thread(None, self.run, None, (), {})
        self.thread.start()

    def run(self):

        while self.toTerminate == False:
            if self.dutyCycle > 0:
                time.sleep(self.dutyCycle * self.sliceTime)

            if self.dutyCycle < self.maxCycle:
                time.sleep((self.maxCycle - self.dutyCycle)
                           * self.sliceTime)

        self.terminated = True

    def calculateDutyCycle(self, pid_out): 
        if (pid_out > self.break_point and self.device == 'heat'):
            out = 99
        elif (-pid_out >self.break_point and self.device == 'cool'):
            out = 100
        else:
            if self.device == 'heat':
                if pid_out < self.hysteresis:
                    return 0
                else:
                    a = 100  / (self.break_point - self.hysteresis)
                    b = 100 - self.break_point * a
                    out = a * pid_out + b
                    if out>=100:
                        out=99
            elif self.device == 'cool':
                pid_out=-pid_out
                if pid_out < self.hysteresis:
                    return 0
                else:
                    a = 100 / (self.break_point - self.hysteresis)
                    b = 100 - self.break_point * a
                    out = a * pid_out + b
        return out

    def changeDutyCycle(self, dutyCycle):

        self.dutyCycle = dutyCycle

    def changeFrequency(self, frequency):

        self.baseTime = 1.0 / frequency
        self.sliceTime = self.baseTime / self.maxCycle
        
        
    def changeBreakPoint(self, break_point):
        
        if break_point>2*self.hysteresis:
            self.break_point=break_point
        else:
            self.break_point=2*self.hysteresis
        
    def changeHysteresis(self, hysteresis):
        if 2*hysteresis<self.break_point:
            self.hysteresis=hysteresis
        else:
            self.hysteresis=self.break_point/2
            
    def changeKp(self,P):
        
        self.Kp=P
        
    def reset(self,device):
        if device == "cooling":   
            self.break_point = 0.8
            self.hysteresis = 0.1
        if device == "heating":    
            self.break_point = 2
            self.hysteresis = 0.1

    def stop(self):

        self.toTerminate = True
        while self.terminated == False:

            time.sleep(0.01)

cooling=pwm(60,0.8,0.1,"cool")
heating=pwm(60,2,0.1,"heat")


