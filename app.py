from flask import Flask, render_template, request, url_for, flash, redirect
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'bf3066a92e1b3c5cbfcd178780a93505'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    #image = db.Column(db.String(20), nullable=False, unique=True, default='default.jpg')

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.password}', '{self.date_joined}')"

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        users = User.query.all()
        return render_template("home.html", profiles=users)
    else:
        return redirect('/')

@app.route('/add_profile', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route('/add', methods=['GET', 'POST'])
def add():
    un = request.form.get("username")
    password = request.form.get("password")
    print(un,password)
    if(un !='' and password != ''):
        new= User(username=un, password=password)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('home'))


    #return render_template("login.html", title="Login", form=form)

@app.route('/delete/<int:id>', methods=['GET'])
def deleted():
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
        
    return redirect(url_for('home'))

app.run(use_reloader=True)