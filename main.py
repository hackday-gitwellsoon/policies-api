from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)