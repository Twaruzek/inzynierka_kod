from flask import Flask, Blueprint, render_template, request
from led import *

from relay import relay_o

from temperature import read_temp
from pwm import cooling, heating 
from pid import pid_h, pid_c
from controller import controller_h, controller_c

main = Blueprint('main', __name__,)
control = Blueprint('control', __name__,)
anakysis = Blueprint('anakysis', __name__,)
project = Blueprint('project', __name__,)
parameters=Blueprint('parameters', __name__,)

@main.route('/')
def index():
	return render_template('index.html')

	

@control.route('/', methods=['POST','GET'])
def panel():
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
    temperature_set=[None]*4
    now=read_temp()
    for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))

    if request.method == 'POST' and 'kitchen' in request.form:
        color= request.form['kitchen']
        kitchen.change_color_string(color)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
    if request.method == 'POST' and 'hall' in request.form:
        color= request.form['hall']
        hall.change_color_string(color)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
    if request.method == 'POST' and 'living_room' in request.form:
        color= request.form['living_room']
        living_room.change_color_string(color)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
    if request.method == 'POST' and 'bathroom' in request.form:
        color= request.form['bathroom']
        bathroom.change_color_string(color)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))

    if request.method == 'POST' and 'heating' in request.form:
        if controller_h.state == 1:
            temperature = request.form['heating']
            pid_h.setPoint(float(temperature))
            temperature_set[0]=1
            temperature_set[1]=0  
        temperature_set[2]=float(pid_h.getPoint())
        temperature_set[3]=float(pid_c.getPoint())
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))   
 
    if request.method == 'POST' and 'cooling' in request.form:
        if controller_c.state == 1:
            temperature = request.form['cooling']
            pid_c.setPoint(float(temperature))
            temperature_set[0]=0
            temperature_set[1]=1
        temperature_set[2]=float(pid_h.getPoint())
        temperature_set[3]=float(pid_c.getPoint())
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
    return render_template('control.html',color=color_now,state=state_now,relay=relay_now,temperature=temperature_set,now_temp=now) 


@control.route('/<room>/<action>', methods=['POST','GET'])
def led(room,action):
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
    now=read_temp()
    temperature_set=[]
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
    if action == 'on':
        eval(room).turn_on()
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
    elif action == 'off':
        eval(room).turn_off()
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
    return render_template('control.html',color=color_now,state=state_now,relay=relay_now,temperature=temperature_set,now_temp=now)

@control.route('/relay/<number>/<state>')
def relay(number,state):
    now=read_temp()
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
    temperature_set=[None]*4
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
    if state == "1":
        if number == "3":
            if kitchen.get_state() == 1:
                kitchen.turn_on()
            if living_room.get_state() ==1:
                living_room.turn_on()
            if bathroom.get_state() ==1:
                bathroom.turn_on()
            if hall.get_state() ==1:
                hall.turn_on()
        if number == "1":
            controller_h.turn_on()
            temperature_set[0]=1
            relay_o.set_state(11,1)
            relay_o.set_state(12,1)
            

         
        relay_o.set_state(eval(number),1)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
        
    if state == "0":
        if number == "1":
            controller_h.turn_off()
            temperature_set[0]=0
            
        relay_o.set_state(eval(number),0)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
            
    
        
    return render_template('control.html',color=color_now,state=state_now, relay=relay_now,temperature=temperature_set,now_temp=now)

@control.route('/temperature/<HC>/<state>')
def temperature(HC,state):
    now=read_temp()
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    temperature_set=[None]*4
    if HC == "heating":
        if state == "1":
            controller_c.turn_off()
            controller_h.turn_on() 
            relay_o.set_state(11,1)
            relay_o.set_state(12,1)
            relay_o.set_state(1,1)
            temperature_set[0]=1
            temperature_set[1]=0
        if state == "0":
            relay_o.set_state(1,0)
            controller_h.turn_off()
            temperature_set[0]=0
            temperature_set[1]=0
    if HC == "cooling":
        if state == "1":
            controller_h.turn_off()
            controller_c.turn_on()
            relay_o.set_state(1,0)
            relay_o.set_state(2,1)
            relay_o.set_state(11,1)
            relay_o.set_state(12,0) 
            temperature_set[0]=0
            temperature_set[1]=1
        if state == "0":
            print("coool 0")
            controller_c.turn_off()
            relay_o.set_state(11,1)
            relay_o.set_state(12,1) 
            temperature_set[0]=0
            temperature_set[1]=0
    
    temperature_set[2]=pid_h.getPoint()
    temperature_set[3]=pid_c.getPoint()
    relay_now=[]
    
    for i in range(1, 9):
        relay_now.append(relay_o.read_state(i))
        
    return render_template('control.html',color=color_now,state=state_now, relay=relay_now,temperature=temperature_set,now_temp=now)



@parameters.route('/')
def parametr():
    heating=[None]*3
    cooling=[None]*3
    if request.method == 'POST' and 'CK' in request.form:
        K = request.form['CK']
        pid_c.setKp(float(K))
    if request.method == 'POST' and 'CKd' in request.form:
        Kd = request.form['CKd']
        pid_c.setKp(float(Kd))
    if request.method == 'POST' and 'CKi' in request.form:
        Ki = request.form['CKi']
        pid_c.setKp(float(Ki))
    if request.method == 'POST' and 'HK' in request.form:
        K = request.form['HCK']
        pid_h.setKp(float(K))
    if request.method == 'POST' and 'HKd' in request.form:
        Kd = request.form['HCKd']
        pid_h.setKp(float(Kd))
    if request.method == 'POST' and 'HKi' in request.form:
        Ki = request.form['HKi']
        pid_h.setKp(float(Ki))

    heating[0]=round(pid_h.Kp,2)
    heating[1]=round(pid_h.Ti,2)
    heating[2]=round(pid_h.Td,2)
    cooling[0]=round(pid_c.Kp,2)
    cooling[1]=round(pid_c.Ti,2)
    cooling[2]=round(pid_c.Td,2)
    return render_template('reg.html',pid_cool=cooling,pid_heat=heating)



@anakysis.route('/')
def test():
    return render_template('index.html')



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