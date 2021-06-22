"""The initial file of the program.

Its responsible for various important pieces of data, such as the
Flask app instantiation. 
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

# Flask app & config instantiation

app = Flask(__name__)
app.config.from_object(Config)


# Database and login instantiation

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


# Lorum Ipsum content for feed

feed_content = list()
MAX = 60
SEND = 10
HEADING = "Lorem ipsum dolor sit amet."
CONTENT = """
Lorem ipsum dolor sit amet consectetur, adipisicing elit.
 Repellat inventore assumenda laboriosam,
 obcaecati saepe pariatur atque est? Quam, molestias nisi.
"""

for x in range(MAX):
    feed_content.append([HEADING, CONTENT])

from app import routes
