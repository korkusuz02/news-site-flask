from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

DB_NAME='dreamlist.db'
app=Flask(__name__)
app.config['SECRET_KEY']="bcvbcvbvb"
app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{DB_NAME}"
db=SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20), nullable=False)
    surname=db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(25), nullable=False)
    password=db.Column(db.String(15), nullable=False)

@app.route("/")
def home():
    return  redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        name=request.form.get('name')
        surname=request.form.get('surname')
        email=request.form.get('email')
        password=request.form.get('password')

        search=Users.query.filter_by(email=email).first()

        if search !=None:
            flash("Bu email ile bir hesap zaten var!!")
            return render_template('register.html')
        new_user=Users(name=name, surname=surname,
                    email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")

        search=Users.query.filter_by(email=email).first()
        if search is None:
            flash('Böyle bir kullanıcı bulunamadı!!')
            return render_template('login.html')
            
        if password==search.password:
            session['email']=email
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for('login'))

if __name__=='__main__':
    if not os.path.exists(DB_NAME):
        db.create_all(app=app)
    app.run(debug=True)