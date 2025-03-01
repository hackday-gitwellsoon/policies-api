from flask import Flask, render_template, request, url_for, redirect, make_response, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

SECRET_KEY = "Preschool3-Duration5-Strum1-Tigress0-Shove8-Scenic3-Unaligned6-Nerd7-Reforest0-Produce8"
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class documents(db.Model):
	_id = db.Column("Policy_ID", db.Integer, primary_key=True)
	title = db.Column("Title", db.String)
	description = db.Column("Description", db.String)
	def __init__(self, title, description):
		self.title = title
		self.description = description

@app.route('/')
def hello():
	test = documents.query.filter_by(_id = 1).first()
	return "hello world"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)