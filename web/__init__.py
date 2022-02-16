from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from os import path
from .camera import Camera
from .led import Led

db = SQLAlchemy()
cam = Camera()
led = Led()

def create_app():
	app = Flask(__name__)
	app.secret_key = "test"
	app.permanent_session_lifetime = timedelta(days=4)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	from .routes import routes

	app.register_blueprint(routes, url_prefix='/')

	from .models import users, animals, live

	create_database(app)

	return app

def create_database(app):
	if not path.exists('web/database'):
		db.create_all(app=app)

