from flask import render_template,request,redirect,url_for,flash,session
from login import admin
from flask.views import MethodView
from PFS import db
from feedback.models import User

class Sign(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        count = db.session.query(User).filter(User.UserName == username).filter(User.Password == pwd).count()
        if count >0:
            session['admin'] = username
            return redirect(url_for('back.feedback_list'))
        flash("用户名或密码错误")
        return render_template('login.html')

admin.add_url_rule('/login/',view_func=Sign.as_view('sign'))

@admin.route('/exit/')
def exit():
    session.pop('admin')
    return redirect(url_for('back.feedback_list'))
