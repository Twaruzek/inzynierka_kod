###########################
### Initialization file ###
###########################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from relay import relay
from led import kitchen, bathroom, hall, living_room



app = Flask(__name__)


app.register_blueprint(main)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY']='nQ{j65rLbt|3#*~fEmwRQ&5HbHNXHK'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

relay = relay()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

migrate = Migrate(app, db)

@app.errorhandler(404)
def not_found(error):
    return 'kotlecik'#render_template('404.html'), 404

