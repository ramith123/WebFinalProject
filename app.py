import os
from flask import Flask, request, render_template
from model import db, User

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hxzhttja:6A7fF17bjLUaeditu817xyU7x0AOzZTh@drona.db.elephantsql.com:5432/hxzhttja'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  # app.config['SECRET_KEY'] = "c3a93f55-2015-4042-9ef7-77de85976f78"
  # app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
@app.route('/')
def hello():
    return app.send_static_file("page.html")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
