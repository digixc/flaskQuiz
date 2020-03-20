from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
 
# get the absolute path to this file
ROOT = os.path.abspath(os.path.dirname(__file__))
DATABASE_NAME = 'quiz.db'

dbPath = os.path.join(ROOT, DATABASE_NAME)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ dbPath
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username


class Quiz(db.Model):
	 
	id = db.Column(db.Integer, primary_key=True)
	quizname = db.Column(db.String(80), unique=False, nullable=False)
	questions = db.relationship('Question', backref='quiz',
                        lazy='dynamic')
	#score = db.Column(db.Integer(20), unique=False, nullable=False)

class Question(db.Model):
	 
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(5), unique=True, nullable=False)
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
	options = db.relationship('Choices', backref='question',
                            lazy='dynamic')
class Results(db.Model):
	 
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
	quiz_date = db.Column(db.DateTime, nullable=False)
	score = db.Column(db.Integer, unique=False, nullable=False)


class Choices(db.Model):
	 
	id = db.Column(db.Integer, primary_key=True)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
	choice = db.Column(db.String(5), unique=False, nullable=False)
	correct= db.Column(db.String(5), unique=False, nullable=False)

def setup():
	db.create_all()
	u = User(username='cthom', email='cthom@hotmail.com', password = '1111')
	db.session.add(u)
	db.session.commit() 

if __name__ == "__main__":
	setup()
