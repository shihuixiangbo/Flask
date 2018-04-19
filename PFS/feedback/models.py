from datetime import datetime
from PFS import db

class Category(db.Model):
    """分类表"""
    __tablename__ = 'category'

    ID = db.Column(db.Integer,primary_key=True)
    CategoryName = db.Column(db.String)

    def __init__(self,CategoryName):
        self.CategoryName = CategoryName

    def __repr__(self):
        return '<部门>{}:{}'.format(self.id,self.CategoryName)

class Feedback(db.Model):
    """反馈表"""
    __tablename__ = 'feedback'

    ID = db.Column(db.Integer,primary_key=True)
    Subject = db.Column(db.String)
    CategoryID = db.Column(db.Integer,db.ForeignKey('category.ID'))
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    Image = db.Column(db.String)
    Body = db.Column(db.String)
    State = db.Column(db.Boolean)
    Reply = db.Column(db.String)
    ReleaseTime = db.Column(db.DateTime)

    category = db.relationship('Category',backref=db.backref('feedbacks',lazy='dynamic'))

    def __init__(self,Subject=None,Username=None,Email=None,Image=None,Body=None,State=None,Reply=None,ReleaseTime=None):
        self.Subject = Subject
        self.Username = Username
        self.Email = Email
        self.Image = Image
        self.Body = Body
        self.State = State
        self.Reply = Reply
        self.ReleaseTime = ReleaseTime if ReleaseTime else datetime.now()

    def __repr__(self):
        return '<反馈>{}'.format(self.Subject)


class User(db.Model):
    """用户信息"""
    __tablename__ = 'user'

    UserName = db.Column(db.String,primary_key=True)
    Email = db.Column(db.String)
    Password = db.Column(db.String)

    def __init__(self,UserName,Email,Password):
        self.UserName = UserName
        self.Email = Email
        self.Password = Password

    def __repr__(self):
        return '<用户:{}>'.format(self.UserName)
