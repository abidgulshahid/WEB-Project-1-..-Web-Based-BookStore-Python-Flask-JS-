from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Register(db.Model):
    __table__name = 'register'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    username = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
	