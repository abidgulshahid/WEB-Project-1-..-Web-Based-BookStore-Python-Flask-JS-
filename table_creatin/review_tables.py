from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Review(db.Model):
    __table__name = 'review'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False)
    isbn = db.Column(db.String,nullable=False)
    review = db.Column(db.String,nullable=False)
    rating = db.Column(db.String,nullable=False)
	
