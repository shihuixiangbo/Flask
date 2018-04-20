from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key="khhskdhskhds"

db = SQLAlchemy(app)

@app.route('/')
def index():
        from person.models import Question

        key = request.args.get('key', '')
        questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()

        # questions = db.session.query(Question).order_by('-id').all()

        return render_template('index.html',questions = questions)

class Login(MethodView):
    def get(self):
        from person.models import Question
        key = request.args.get('key', '')
        if key:
            questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()
            return render_template('index.html', questions=questions)

        return render_template('login.html')

    def post(self):
        from person.models import User
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = db.session.query(User).filter(User.telephone == telephone).filter(User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 在31天免登入
            session.permanent = True
            return redirect(url_for('index'))
        flash("用户名或密码错误")
        return render_template('login.html')

app.add_url_rule('/login/',view_func=Login.as_view('login'))


class Regist(MethodView):
    def get(self):
        from person.models import Question
        key = request.args.get('key', '')
        if key:
            questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()
            return render_template('index.html', questions=questions)
        return render_template('regist.html')

    def post(self):
        from person.models import User
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
                user = User(username,telephone,password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

app.add_url_rule('/regist/',view_func=Regist.as_view('regist'))

class Question(MethodView):
    def get(self):
        from person.models import Question
        key = request.args.get('key', '')
        if key:
            questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()
            return render_template('index.html', questions=questions)

        if session.get('user_id', None) is None:
            return redirect(url_for('login'))
        return render_template('question.html')

    def post(self):
        from person.models import Question

        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title,content)

        question.author_id = session.get('user_id')

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

app.add_url_rule('/question/',view_func=Question.as_view('question'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    from person.models import Question
    key = request.args.get('key', '')
    if key:
        questions = db.session.query(Question).filter(Question.title.contains(key)).order_by('-id').all()
        return render_template('index.html',questions = questions)

    question = db.session.query(Question).filter(Question.id == question_id).first()

    return render_template('detail.html',question = question)

@app.route('/add_answer/',methods=['POST'])
def add_answer():
    from person.models import Answer,User

    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    
    content = request.form.get('answer_content')
    answer = Answer(content)

    answer.question_id = request.form.get('question_id')

    answer.author_id = session['user_id']

    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail',question_id = answer.question_id))

if __name__ == '__main__':
    app.run()
