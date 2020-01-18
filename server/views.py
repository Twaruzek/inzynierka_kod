from flask import Flask, Blueprint, render_template, request
from led import *
from relay import *

main = Blueprint('main', __name__,)
control = Blueprint('control', __name__,)
anakysis = Blueprint('anakysis', __name__,)
project = Blueprint('project', __name__,)

@main.route('/')
def index():
	return render_template('index.html')

	

@control.route('/', methods=['POST','GET'])
def panel():
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
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
    return render_template('control.html',color=color_now,state=state_now,relay=relay_now)
 
    


@control.route('/<room>/<action>', methods=['POST','GET'])
def led(room,action):
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
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
    return render_template('control.html',color=color_now,state=state_now,relay=relay_now)

@control.route('/relay/<number>/<state>')
def relay(number,state):
    color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
    state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
    relay_now=[]
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
            
        relay_o.set_state(eval(number),1)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
        
    if state == "0":
        relay_o.set_state(eval(number),0)
        color_now = [kitchen.get_color(),hall.get_color(),living_room.get_color(),bathroom.get_color()]
        state_now = [kitchen.get_state(),hall.get_state(),living_room.get_state(),bathroom.get_state()]
        relay_now=[]
        for i in range(1, 9):
            relay_now.append(relay_o.read_state(i))
        
    return render_template('control.html',color=color_now,state=state_now, relay=relay_now)


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