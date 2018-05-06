from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)

    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref='questions')

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)

    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    question = db.relationship('Question',backref=db.backref('answers',order_by = create_time.desc()))

    author = db.relationship('User',backref='answers')

