from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Books(db.Model):
    __table__name = 'books'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    author = db.Column(db.String,nullable=False)
    isbn = db.Column(db.String,nullable=False)
    year = db.Column(db.String,nullable=False)
	
