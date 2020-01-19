#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import threading
import w1thermsensor
import RPi.GPIO as GPIO
import math
GPIO.setmode(GPIO.BCM)



class pwm(threading.Thread):

    def __init__(
        self,
        frequency,
        P,
        break_point,
        hysteresis,
        device,
        ):
        """ 
     Init the PiZyPwm instance. Expected parameters are :
     - frequency : the frequency in Hz for the PWM pattern. A correct value may be 100.
     - gpioPin : the pin number which will act as PWM ouput
     - gpioScheme : the GPIO naming scheme (see RPi.GPIO documentation)
     """

        self.break_point = break_point
        self.Kp = P
        self.hysteresis = hysteresis
        self.device = device

        self.baseTime = 1.0 / frequency
        self.maxCycle = 100.0
        self.sliceTime = self.baseTime / self.maxCycle
        self.terminated = False
        self.toTerminate = False

     # GPIO.setmode(gpioScheme)

    def start(self, dutyCycle):
        """
    Start PWM output. Expected parameter is :
    - dutyCycle : percentage of a single pattern to set HIGH output on the GPIO pin
    
    Example : with a frequency of 1 Hz, and a duty cycle set to 25, GPIO pin will 
    stay HIGH for 1*(25/100) seconds on HIGH output, and 1*(75/100) seconds on LOW output.
    """

        self.dutyCycle = dutyCycle
        self.thread = threading.Thread(None, self.run, None, (), {})
        self.thread.start()

    def run(self):
        """
    Run the PWM pattern into a background thread. This function should not be called outside of this class.
    """

        while self.toTerminate == False:
            if self.dutyCycle > 0:
                time.sleep(self.dutyCycle * self.sliceTime)

            if self.dutyCycle < self.maxCycle:
                time.sleep((self.maxCycle - self.dutyCycle)
                           * self.sliceTime)

        self.terminated = True

    def calculateDutyCycle(self, pid_out):
        pid_out = pid_out / self.Kp
        print(pid_out)
        if pid_out > self.break_point:
            out = 100
        else:
            if self.device == 'heat':
                if pid_out > 0:
                    return 0
                a = 100  / (self.break_point - self.hysteresis)
                b = 100 - self.break_point * a
                out = -a * pid_out + b
            elif self.device == 'cool':
                if pid_out <0:
                    return 0
                a = 100 / (self.break_point - self.hysteresis)
                b = 100 - self.break_point * a
                out = a * pid_out + b
            
        return out

    def changeDutyCycle(self, dutyCycle):
        """
    Change the duration of HIGH output of the pattern. Expected parameter is :
    - dutyCycle : percentage of a single pattern to set HIGH output on the GPIO pin
    
    Example : with a frequency of 1 Hz, and a duty cycle set to 25, GPIO pin will 
    stay HIGH for 1*(25/100) seconds on HIGH output, and 1*(75/100) seconds on LOW output.
    """

        self.dutyCycle = dutyCycle

    def changeFrequency(self, frequency):
        """
    Change the frequency of the PWM pattern. Expected parameter is :
    - frequency : the frequency in Hz for the PWM pattern. A correct value may be 100.
    
    Example : with a frequency of 1 Hz, and a duty cycle set to 25, GPIO pin will 
    stay HIGH for 1*(25/100) seconds on HIGH output, and 1*(75/100) seconds on LOW output.
    """

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

    def stop(self):
        """
    Stops PWM output.
    """

        self.toTerminate = True
        while self.terminated == False:

      # Just wait

            time.sleep(0.01)

    # pi.write_byte_data(address,0x26,self.gpioPin)

        GPIO.output(self.gpioPin, GPIO.LOW)
        GPIO.setup(self.gpioPin, GPIO.IN)


# motor = pwm(100,8)
# motor.start(100)
