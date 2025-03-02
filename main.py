import os
from dataclasses import dataclass
from admin.documentadmin import DocumentAdmin
from admin.hospitaladmin import HospitalAdmin

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "git")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", 'sqlite:///database.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)

@dataclass
class Documents(db.Model):
	_id: int
	title: str
	description: str
	hospital_id: str

	_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	description = db.Column(db.Text)

	hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
	hospital = db.relationship('Hospitals', backref=db.backref('documents', lazy=True))

	def __str__(self):
		return f"{self.jurisdiction} / {self.name}"

@dataclass
class Hospitals(db.Model):
	_id: int
	jurisdiction: str
	board: str
	name: str

	_id = db.Column("id", db.Integer, primary_key=True)
	jurisdiction = db.Column("jurisdiction", db.String(255))
	board = db.Column("board", db.String(255))
	name = db.Column("name", db.String(255))

with app.app_context():
    db.create_all()

admin = Admin(app, name='Policy Admin', template_mode='bootstrap4')
admin.add_view(DocumentAdmin(Documents, db.session))
admin.add_view(HospitalAdmin(Hospitals, db.session))

@app.route('/')
def hello():
	return jsonify(Documents.query.all())

@app.route('/get_all_hospitals')
def get_all_hospitals():
	return jsonify(Hospitals.query.all())

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