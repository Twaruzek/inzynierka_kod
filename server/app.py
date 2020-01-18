from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from relay import GPIO




from views import *
from temperature import read_temp
#from model import record
from relay import relay

from sys import path
from os import getcwd, name
splitter = '\\' if name == 'nt' else '/'
path.append(
    splitter.join(
        getcwd().split(
            splitter
        )[:-1]
    )
)

from flask_colorpicker import colorpicker

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://server/db.db'
app.config['SECRET_KEY']='nQ{j65rLbt|3#*~fEmwRQ&5HbHNXHK'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(main)
app.register_blueprint(control, url_prefix="/control")
app.register_blueprint(anakysis, url_prefix="/anakysis")
app.register_blueprint(project, url_prefix="/project")




GPIO.setwarnings(False)


colorpicker(app, local=['static/spectrum.js', 'static/spectrum.css'])



#print(relay)

	
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
		
#if __name__ == "__main__":
#    app.run(host='0.0.0.0', debug=True)

