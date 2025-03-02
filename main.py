from io import BytesIO
import os
from dataclasses import dataclass
from admin.documentadmin import DocumentAdmin
from admin.hospitaladmin import HospitalAdmin

from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from weasyprint import HTML

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

	def __str__(self):
		return f"{self.jurisdiction} / {self.board} / {self.name}"

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


@app.route('/documents')
def document_filter():
	search_query = request.args.get('search_query', default="", type=str)
	filter_by = request.args.get('filter_by', default="Title", type=str)
	hospital_query = request.args.get('hospital_id', default="", type=int)

	hospital_results = Documents.query.filter(Documents.hospital_id == hospital_query)

	if filter_by == 'Title':
		results  = hospital_results.query.filter(Documents.title.ilike(f"%{search_query}%"))
	elif filter_by == 'Description':
		results = hospital_results.query.filter(Documents.description.ilike(f"%{search_query}%"))
	else:
		return "error filter not found."
	return jsonify(results.all())

@app.route('/document_by_id/<id>')
def document(id):
	document = Documents.query.get_or_404(id)
	return jsonify(document)

@app.route('/hospitals')
def hospital_filter():
	search_query = request.args.get('search_query', default="", type=str)
	results = Hospitals.query.filter(Hospitals.name.ilike(f"%{search_query}%"))
	return jsonify(results.all())

@app.route('/download/<id>', methods=['GET'])
def download(id):
    document = Documents.query.get_or_404(id)
    html_content = f"""
    <h1>{document.title}</h1>
    {document.description}
    """
    pdf_file = BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    return send_file(pdf_file, download_name=f"{document.title}.pdf", as_attachment=True)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)