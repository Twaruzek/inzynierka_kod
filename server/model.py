from sqlalchemy import Column, Integer, String
from datetime import datetime
from app import db

class record(db.Model):
    time = db.Column(db.Datetime, primary_key=True, default=db.func.current_timestamp())
    temperature = db.Column(db.Float)

    
    
