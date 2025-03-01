from flask import Flask, render_template, request, url_for, redirect, make_response, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

SECRET_KEY = "git"
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
def Hello():
	# test = documents.query.all()
	# query = jsonify(({'title': test.title, 'description': test.description}))
	# return query
	filter_name = request.args.get("Title")
	filter_description = request.args.get("Description")

	if filter_name:
		query = query.filter(documents.title.ilike(f"%{filter_name}"))
	if filter_description:
		query = query.filter(documents.description.ilike(f"%{filter_description}"))
	results = query.all()
	response = ({'title': Doc.title, 'description': Doc.description} for Doc in results)
	return jsonify(response)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)