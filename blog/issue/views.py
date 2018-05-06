from flask import Blueprint,render_template,request,redirect,url_for,session
from flask.views import MethodView
from exts import db
from models import User,Question,Answer
from decorators import login_required

issues = Blueprint('issues',__name__)

class Questions(MethodView):
    @login_required
    def get(self):
        return render_template('question.html')

    def post(self):
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)

        question.author_id = session.get('user_id')

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

issues.add_url_rule('/question/',view_func=Questions.as_view('question'))

@issues.route('/detail/<question_id>/')
def detail(question_id):
    question = db.session.query(Question).filter(Question.id == question_id).first()
    count = db.session.query(Answer).filter(Answer.question_id == question_id).count()

    return render_template('detail.html',question = question,count=count)

@issues.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    answer = Answer(content=content)

    answer.question_id = request.form.get('question_id')
    answer.author_id = session['user_id']

    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('issues.detail', question_id=answer.question_id))
