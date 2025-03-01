from dataclasses import dataclass
from flask import Flask, render_template, request, url_for, redirect, make_response, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

SECRET_KEY = "git"
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@dataclass
class Documents(db.Model):
	_id: int
	title: str
	description: str

	_id = db.Column("Policy_ID", db.Integer, primary_key=True)
	title = db.Column("Title", db.String)
	description = db.Column("Description", db.String)

@dataclass
class Hospitals(db.Model):
	_id: int
	jurisdiction: str
	board: str
	name: str

	_id = db.Column("id", db.Integer, primary_key=True)
	jurisdiction = db.Column("jurisdiction", db.String)
	board = db.Column("board", db.String)
	name = db.Column("name", db.String)

with app.app_context():
    db.create_all()

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Documents, db.session))
admin.add_view(ModelView(Hospitals, db.session))
# Add administrative views here


# @app.route('/')
# def hello():
# 	return jsonify(Documents.query.all())

@app.route('/get_all_hospitals')
def get_all_hospitals():
	return jsonify(Hospitals.query.all())
# @app.route('/')
# @app.route('/documents?query="<string:query>"&filter="<string:filter>"',methods=['GET','POST'])
# def load_defaults(query, filter):
@app.route('/documents')
def load_defaults():

	search_query = request.args.get('search_query', default="", type=str)
	filter_by = request.args.get('filter_by', default="Title", type=str)

	if filter_by == 'Title':
		results  = Documents.query.filter(Documents.title.ilike(f"%{search_query}%"))
	elif filter_by == 'Description':
		results = Documents.query.filter(Documents.description.ilike(f"%{search_query}%"))
	else:
		return "hello world"

	response = [{'title': doc.title, 'description': doc.description} for doc in results.all()]
	return jsonify(response)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)