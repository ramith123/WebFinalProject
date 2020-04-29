import os,json
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from model import db, User
from forms import Register, Login


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hxzhttja:6A7fF17bjLUaeditu817xyU7x0AOzZTh@drona.db.elephantsql.com:5432/hxzhttja'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "c3a93f55-2015-4042-9ef7-77de85976f78"
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()


@app.route('/')
def hello():
    return app.send_static_file("page.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = Register()
  if form.validate_on_submit():
    data = request.form
    x = User.query.filter_by(username = data['username']).count()
    if(x>0):
      flash('That username is already taken, please choose another')
      return render_template('register.html', form=form) 
    else:
      newuser = User(username=data['username']) # , email=data['email']
      newuser.set_password(data['password']) 
      db.session.add(newuser) 
      db.session.commit()
      flash('Account Created!')
      return redirect(url_for('login'))
  return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = Login()
  if form.validate_on_submit():
    data = request.form
    user = User.query.filter_by(username = data['username']).first()
    if user and user.check_password(data['password']): 
      flash('Logged in successfully.') 
      login_user(user)
      return redirect(url_for('loginTest'))
    else:
      flash('Invalid username or password') 
      return redirect(url_for('login'))
  return render_template('login.html', form=form) 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('hello'))

@app.route('/loginTest', methods=['GET'])
def loginTest():
  return render_template('testlogin.html')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
