from flask import Flask
from models import db, bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')

bcrypt.init_app(app)
db.init_app(app)

# todo: need to create database

if __name__ == '__main__':
    app.run()