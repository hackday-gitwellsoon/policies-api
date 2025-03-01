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

class documents(db.Model):
	_id = db.Column("Policy_ID", db.Integer, primary_key=True)
	title = db.Column("Title", db.String)
	description = db.Column("Description", db.String)
	def __init__(self, title, description):
		self.title = title
		self.description = description

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(documents, db.session))
# Add administrative views here


@app.route('/')
def hello():
	test = documents.query.all()
	query = jsonify(({'title': test.title, 'description': test.description}))
	return query


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)