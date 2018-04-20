from datetime import datetime
from demo import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    telephone = db.Column(db.String(11))
    password = db.Column(db.String(100))

    def __init__(self,username=None,telephone=None,password=None):
        self.username = username
        self.telephone = telephone
        self.password = password

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)

    author_id = db.Column(db.String(100),db.ForeignKey('user.id'))

    author = db.relationship('User',backref='questions')


    def __init__(self, title,content):
        self.title = title
        self.content = content


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('user.id'))

    question = db.relationship('Question',backref=db.backref('answers',order_by = id.desc()))

    author = db.relationship('User',backref='answers')

    def __init__(self,content):
        self.content = content




