from flask import Flask, session,render_template,request,flash
from flask_session import Session
from sqlalchemy import create_engine
import json
import os
import requests
from sqlalchemy.orm import scoped_session, sessionmaker
# Check for environment variable
app = Flask(__name__)
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"]= "hackerone231"
Session(app)


# Set up database
link = "postgres://iaduovpmoevsrt:8225056ab265e9a1818951bbc9ce12c730b1b47adf319afae2b41e7f1360c63d@ec2-54-235-193-0.compute-1.amazonaws.com:5432/de3f75hci6d3hk" 
engine = create_engine(link)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/register",methods=["GET","POST"])
def register():
	name = request.form.get("name")
	username = request.form.get("username")
	email = request.form.get("email")
	password = request.form.get("password")
	if request.method== "POST":
		username_validity_query = db.execute("SELECT username FROM register WHERE username=:username",{"username":username}).fetchone()
		if username_validity_query is not None:
			error_username_validity = "Username Already Existed"
			return render_template("index.html",error_username_validity=error_username_validity)
		
		else:
			register_query = db.execute("INSERT INTO register (name,username,email,password) VALUES  (:name,:username,:email,:password) ",{"name":name,"username":username,"email":email,"password":password})
			if register_query:
				db.commit()
				success = name + " You can Login Now"
				return render_template("index.html",success=success)

	else:
		return render_template("index.html")


@app.route("/search",methods=["GET","POST"])
def search():
	username = request.form.get("username")
	password = request.form.get("password")


	if request.method == "POST":
		name_query = db.execute("SELECT username FROM register WHERE username=:username",{"username":username}).fetchone()
		db.commit()
		login_query = db.execute("SELECT username,password FROM register WHERE username=:username AND password=:password",{"username":username,"password":password}).fetchone()
		db.commit()
		session["username"] = username
		if login_query:
			return render_template("home.html",name=name_query)
		else:
			username_error ="Username or Password Incorrect"
			return render_template("index.html",username_error=username_error)
	else:
		return render_template("index.html")

@app.route("/api/<string:isbn>",methods=["GET","POST"])

def api(isbn):
	request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vguAWxSWysSfur23uFOPg", "isbns": isbn})
	result_query = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
	average_rating=request.json()['books'][0]['average_rating']
	work_ratings_count=request.json()['books'][0]['work_ratings_count']
	api_query = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
	if api_query == None:
		return render_template("error.html")
	data = {"title" : api_query.title,"author": api_query.author,"year":api_query.year,"isbn":api_query.isbn,"review_count":work_ratings_count,"average_score":average_rating}
	dump = json.dumps(data)
	return render_template("api.html",api=dump)
@app.route("/result",methods=["GET","POST"])
def result():
	search = request.form.get("search")

	if request.method == "POST":
		search_query=db.execute("SELECT * FROM books WHERE author iLIKE '%"+search+"%' OR title iLIKE '%"+search+"%' OR isbn iLIKE '%"+search+"%'").fetchall()

		#search_query = db.execute("SELECT * FROM books WHERE title=:title OR isbn=:isbn OR author=:author",{"title":search,"isbn":search,"author":search}).fetchall()
		db.commit()
		if search_query:
			results = len(search_query)
			return render_template("search.html",search_query=search_query,results=results)
		elif len(search_query) == 0:
			search_error = search + " Not Found"
			return render_template("home.html",search_error=search_error)
	else:
		return render_template("index.html")


@app.route("/bookpage/<string:isbn>",methods=["GET","POST"])
def bookpage(isbn):
	
	request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vguAWxSWysSfur23uFOPg", "isbns": isbn})
	result_query = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
	average_rating=request.json()['books'][0]['average_rating']
	work_ratings_count=request.json()['books'][0]['work_ratings_count']
    # return 
	return render_template("result.html",result_query=result_query,average=average_rating,work_ratings_count=work_ratings_count)

@app.route("/review/<string:isbn>",methods=["GET","POST"])
def review(isbn):
	username=session['username']
	rating = request.form.get("rating")
	review = request.form.get("review")
	dupp = db.execute("SELECT * FROM review WHERE isbn=:isbn AND username=:username",{"isbn":isbn,"username":session['username']})
	if request.method == "POST":
		if dupp == None:
			if review != None and rating != None:
				success = db.execute("INSERT INTO review (username,isbn,review,rating) VALUES (:username,:isbn,:review,:rating)",{"username":str(session['username']),"isbn":isbn,"review":review,"rating":rating})
				db.commit()
				if success:
					return "Success added "+ review
				else:
					return "Wrong"
		else:
			return render_template("result.html",review_error="Your Rating And Review Are Already Existed")
	else:
		return render_template("result.html") 
@app.route("/update")
def update():
	pass

@app.route("/admin_login")
def admin_login():
	return "UNDER CONSTRUCTION"

@app.route("/admin",methods=["GET","POST"])
def admin():
	if request.method== "POST":
		admin_query = db.execute("SELECT * FROM register").fetchall()
		db.commit()
		if admin_query:
			return render_template("admin.html",admin=admin_query)
	else:
		return render_template("index.html")
	
@app.route("/logout")
def logout():
	session.clear()
	logout_message = "You Have Successfully Logout"
	return render_template("index.html",logout_message=logout_message)

if __name__ == "__main__":
	app.run(debug=True)
