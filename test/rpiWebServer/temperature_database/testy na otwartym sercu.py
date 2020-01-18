import w1thermsensor
import RPi.GPIO as GPIO
import sqlite3 as lite
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)


GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)


GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)





GPIO.setup(7, GPIO.OUT)
ena = GPIO.PWM(7,100)
GPIO.setup(8, GPIO.OUT)
enb = GPIO.PWM(8,100)

ena.start(100)
enb.start(100)

GPIO.setup(15, GPIO.OUT)
enzarowa = GPIO.PWM(15,100)

enzarowa.start(0)

