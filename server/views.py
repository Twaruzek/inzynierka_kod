from flask import Flask, Blueprint, render_template, request
from led import *
import io
from relay import relay_o
from fan_c import fan_c
from temperature import read_temp
from pwm import cooling, heating 
from pid import pid_h, pid_c
from controller import controller_h, controller_c


main = Blueprint('main', __name__,)
control = Blueprint('control', __name__,)
project = Blueprint('project', __name__,)
parameters=Blueprint('parameters', __name__,)


@main.route('/')
def index():
	return render_template('index.html')

	
@control.route('/', methods=['POST','GET'])
def panel():
    now=round(read_temp(),2)
    
##################################
### Methods - LED + TEMP + FAN ###
##################################
    
    if request.method == 'POST' and 'kitchen' in request.form:
        color= request.form['kitchen']
        kitchen.change_color_string(color)

    if request.method == 'POST' and 'hall' in request.form:
        color= request.form['hall']
        hall.change_color_string(color)

    if request.method == 'POST' and 'living_room' in request.form:
        color= request.form['living_room']
        living_room.change_color_string(color)

    if request.method == 'POST' and 'bathroom' in request.form:
        color= request.form['bathroom']
        bathroom.change_color_string(color)

    if request.method == 'POST' and 'heating' in request.form:
        if controller_h.state == 1:
            temperature = request.form['heating']
            pid_h.setPoint(float(temperature))
 
    if request.method == 'POST' and 'cooling' in request.form:
        if controller_c.state == 1:
            temperature = request.form['cooling']
            pid_c.setPoint(float(temperature))
            
    if request.method == 'POST' and 'fan' in request.form:
        fan_c.pwm = request.form['fan']
        relay_o.set_pwm("enb",fan_c.pwm)
        fan_c.state=1
        relay_o.set_state(13,1)
        relay_o.set_state(14,0)



    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
    temperature_set=[None]*4
    temperature_set[0]=controller_h.get_state()
    temperature_set[1]=controller_c.get_state()       
    temperature_set[2]=pid_h.getPoint()
    temperature_set[3]=pid_c.getPoint()
    fan_date = [fan_c.state,fan_c.pwm]
    return render_template('control.html',color=color_now,state=state_now,relay=relay_now,temperature=temperature_set,now_temp=now,fan=fan_date) 


@control.route('/<room>/<action>', methods=['POST','GET'])
def led(room,action):
    now=round(read_temp(),2)
    
##################
### LED ON/OFF ###
##################

    if action == 'on':
        eval(room).turn_on()

    elif action == 'off':
        eval(room).turn_off()

    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
    temperature_set=[None]*4
    temperature_set[0]=controller_h.get_state()
    temperature_set[1]=controller_c.get_state()       
    temperature_set[2]=pid_h.getPoint()
    temperature_set[3]=pid_c.getPoint()
    fan_date = [fan_c.state,fan_c.pwm]
    return render_template('control.html',color=color_now,state=state_now,relay=relay_now,temperature=temperature_set,now_temp=now,fan=fan_date)

@control.route('/relay/<number>/<state>')
def relay(number,state):
    now=round(read_temp(),2)

#############
### Relay ###
#############
    
    if state == "1":
        # LED
        if number == "3":
            if kitchen.get_state() == 1:
                kitchen.turn_on()
            if living_room.get_state() ==1:
                living_room.turn_on()
            if bathroom.get_state() ==1:
                bathroom.turn_on()
            if hall.get_state() ==1:
                hall.turn_on()
        # DIMMER
        if number == "1":
            controller_h.turn_on()
            temperature_set[0]=1
            relay_o.set_state(11,1)
            relay_o.set_state(12,1) 
        relay_o.set_state(eval(number),1)
     
    if state == "0":
        if number == "1":
            controller_h.turn_off()
        relay_o.set_state(eval(number),0)

    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
    temperature_set=[None]*4
    temperature_set[0]=controller_h.get_state()
    temperature_set[1]=controller_c.get_state()       
    temperature_set[2]=pid_h.getPoint()
    temperature_set[3]=pid_c.getPoint()
    fan_date = [fan_c.state,fan_c.pwm]    
    return render_template('control.html',color=color_now,state=state_now, relay=relay_now,temperature=temperature_set,now_temp=now,fan=fan_date)

@control.route('/temperature/<HC>/<state>')
def temperature(HC,state):
    now=round(read_temp(),2)

##############################
### Heating/Cooling ON/OFF ###
##############################
    
    if HC == "heating":
        if state == "1":
            controller_c.turn_off()
            controller_h.turn_on() 
            relay_o.set_state(11,1)
            relay_o.set_state(12,1)
            relay_o.set_state(1,1)
        if state == "0":
            relay_o.set_state(1,0)
            controller_h.turn_off()
            
    if HC == "cooling":
        if state == "1":
            controller_h.turn_off()
            controller_c.turn_on()
            relay_o.set_state(1,0)
            relay_o.set_state(2,1)
            relay_o.set_state(11,1)
            relay_o.set_state(12,0) 
        if state == "0":
            controller_c.turn_off()
            relay_o.set_state(11,1)
            relay_o.set_state(12,1)
            
    if HC == "fan":
        if state == "1":
            fan_c.set_state(1)
            relay_o.set_pwm("enb",fan_c.pwm)
            relay_o.set_state(13,1)
            relay_o.set_state(14,0)
        if state == "0":
            fan_c.set_state(0) 
            relay_o.set_state(13,1)
            relay_o.set_state(14,1)
    
    fan_date = [fan_c.state,fan_c.pwm]
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    temperature_set=[None]*4
    temperature_set[0]=controller_h.get_state()
    temperature_set[1]=controller_c.get_state()    
    temperature_set[2]=pid_h.getPoint()
    temperature_set[3]=pid_c.getPoint()
    relay_now=[]  
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
        
    return render_template('control.html',color=color_now,state=state_now, relay=relay_now,temperature=temperature_set,now_temp=now,fan=fan_date)



@parameters.route('/',methods=['POST','GET'])
def parametr():

###################
### PID + PWM / ###
###################
    
    
    if request.method == 'POST' and 'CK' in request.form:
        try:
            K = request.form['CK']
            pid_c.setKp(float(K))
        except:
            pass
    if request.method == 'POST' and 'CKd' in request.form:
        try:
            Kd = request.form['CKd']
            pid_c.setKd(float(Kd))
        except:
            pass
    if request.method == 'POST' and 'CKi' in request.form:
        try:
            Ki = request.form['CKi']
            pid_c.setKi(float(Ki))
        except:
            pass
    if request.method == 'POST' and 'HK' in request.form:
        try:
            K = request.form['HK']
            pid_h.setKp(float(K))
        except:
            pass
    if request.method == 'POST' and 'HKd' in request.form:
        try:
            Kd = request.form['HKd']
            pid_h.setKd(float(Kd))
        except:
            pass
    if request.method == 'POST' and 'HKi' in request.form:
        try:
            Ki = request.form['HKi']
            pid_h.setKi(float(Ki))
        except:
            pass
        
        
    if request.method == 'POST' and 'CBP' in request.form:
        try:
            x = request.form['CBP']
            cooling.changeBreakPoint(float(x))
        except:
            pass 
    if request.method == 'POST' and 'CHis' in request.form:
        try:
            x = request.form['CHis']
            cooling.changeHysteresis(float(x))
        except:
            pass
        
    if request.method == 'POST' and 'HBP' in request.form:
        try:
            x = request.form['HBP']
            heating.changeBreakPoint(float(x))
        except:
            pass
    if request.method == 'POST' and 'HHis' in request.form:
        try:
            x = request.form['HHis']
            heating.changeHysteresis(float(x))
        except:
            pass
        
    heat=[None]*5
    cool=[None]*5        
    heat[0]=round(pid_h.Kp,2)
    heat[1]=round(pid_h.Ti,2)
    heat[2]=round(pid_h.Td,2)
    heat[3]=round(heating.break_point,2)
    heat[4]=round(heating.hysteresis,2)
    cool[0]=round(pid_c.Kp,2)
    cool[1]=round(pid_c.Ti,2)
    cool[2]=round(pid_c.Td,2)
    cool[3]=round(cooling.break_point,2)
    cool[4]=round(cooling.hysteresis,2)
    return render_template('reg.html',pid_cool=cool,pid_heat=heat)





@parameters.route('/reset/<device>')
def def_value(device):
    heat=[None]*5
    cool=[None]*5
    
#####################
### Reset PID/PWM ###
#####################

    if device == "pid_h":
        pid_h.reset("cooling")
    if device == "pid_c":
        pid_c.reset("heating")
    if device == "sat_h":
        heating.reset("heating")
    if device == "sat_c":
        cooling.reset("cooling")
    
    heat[0]=round(pid_h.Kp,2)
    heat[1]=round(pid_h.Ti,2)
    heat[2]=round(pid_h.Td,2)
    heat[3]=round(heating.break_point,2)
    heat[4]=round(heating.hysteresis,2)
    cool[0]=round(pid_c.Kp,2)
    cool[1]=round(pid_c.Ti,2)
    cool[2]=round(pid_c.Td,2)
    cool[3]=round(cooling.break_point,2)
    cool[4]=round(cooling.hysteresis,2)
    return render_template('reg.html',pid_cool=cool,pid_heat=heat)






@project.route('/assumptions')
def assumptions():
    return render_template('index.html')
@project.route('/authors')
def authors():
    return render_template('index.html')
@project.route('/lab')
def lab():
    return render_template('index.html')
@project.route('/thesis')
def thesis():
    return render_template('index.html')