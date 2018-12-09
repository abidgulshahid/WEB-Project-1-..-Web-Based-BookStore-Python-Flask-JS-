from flask import Flask
from registr_tables import *
link = ""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://iaduovpmoevsrt:8225056ab265e9a1818951bbc9ce12c730b1b47adf319afae2b41e7f1360c63d@ec2-54-235-193-0.compute-1.amazonaws.com:5432/de3f75hci6d3hk"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db.init_app(app)

def index():
    db.create_all()
    print "Table Created"

if __name__ == "__main__":
	with app.app_context():
		index()
