from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id  = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.Text , nullable=False)
    age = db.Column(db.Integer , nullable=False)
    about = db.Column(db.Text )

    @validates('age')
    def validate_age(self ,key , value):
        if not(1<=value):
            raise ValueError("Age must be positive integer")
        return value
    
    def __repr__(self):
        return f'Person with name {self.name} and age {self.age} tell about himself/herself : {self.about}'
    