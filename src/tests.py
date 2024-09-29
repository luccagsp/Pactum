from flask import Flask, render_template
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from getplain import getText
import os

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "mysecretkeyyy"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Crear las tablas al iniciar la app
with app.app_context():
    db.init_app(app)
    db.create_all()  # Esto se asegurará de que las tablas sean creadas

@app.route('/')
def home():
    return getText("./template/index.html")

# if _name_ == "_main_":
#     app.run(debug=True)