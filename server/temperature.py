import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor= '/sys/bus/w1/devices/28-011452cc30aa/w1_slave'

def read_temp_raw():
    f = open(sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    try:
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
    except:
        return(99)

    


