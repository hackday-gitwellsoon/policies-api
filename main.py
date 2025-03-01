from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
SECRET_KEY = "Preschool3-Duration5-Strum1-Tigress0-Shove8-Scenic3-Unaligned6-Nerd7-Reforest0-Produce8"
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class technologies(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)

@app.route('/')
def hello():
	return "Hello World!"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)