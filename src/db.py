from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
# from app import app
global db
db = None

def create_db(app):
    global db  
    class Base(DeclarativeBase):
        pass

    # create the app
    db = SQLAlchemy(model_class=Base)
    db.init_app(app)
    return db