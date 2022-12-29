import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

# this is app instance
app = Flask(__name__)

# Configuration for connecting to the database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ecom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "secretkey"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["jpeg", "jpg", "png"]
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["IMAGE_UPLOADS"] = os.path.join(basedir, "uploads")
db = SQLAlchemy(app)

# define routes
from ecom import routes


