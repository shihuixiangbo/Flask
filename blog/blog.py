from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask.views import MethodView
import config
from exts import db
from models import User,Question

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

from issue.views import issues
app.register_blueprint(issues)

@app.route('/')
def index():
    key = request.args.get('key', '')
    questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-create_time').all()
    return render_template('index.html', questions=questions)

class Login(MethodView):
    def get(self):
        key = request.args.get('key', '')
        if key:
            questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()
            return render_template('index.html', questions=questions)
        return render_template('login.html')

    def post(self):
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = db.session.query(User).filter(User.telephone == telephone).filter(User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        flash("手机号或密码错误")
        return render_template('login.html')

app.add_url_rule('/login/',view_func=Login.as_view('login'))


class Regist(MethodView):
    def get(self):
        key = request.args.get('key', '')
        if key:
            questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()
            return render_template('index.html', questions=questions)
        return render_template('regist.html')

    def post(self):
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果注册了，就不能再注册了
        user = db.session.query(User).filter(User.telephone == telephone).first()

        if user:
            flash('该手机号码已注册，请更换手机号码')
            return redirect(url_for('regist'))
        else:
            #password1要和password2相等才可以
            if password1 != password2:
                flash('两次密码输入不正确，请核对后填写')
                return redirect(url_for('regist'))
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
app.add_url_rule('/regist/',view_func=Regist.as_view('regist'))

@app.route('/exit/')
def exit():
    session.clear()
    return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()
