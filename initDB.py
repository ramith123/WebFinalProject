from app import app
from model import db

# db.init_app(app)
db.create_all(app=app)
