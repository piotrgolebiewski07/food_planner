from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

with app.app_context():
    results = db.session.execute(text('show databases'))
    for row in results:
        print(row)

from food_planner_app import ingredients

