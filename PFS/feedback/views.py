from datetime import datetime
from feedback import back
from flask import request,render_template,url_for,redirect,send_from_directory,session
from PFS import db
from .models import Category,Feedback
import os

UPLOAD_FOLDER = '/Users/wudaqiang/PycharmProjects/production/mysource/flask/PFS/uploads'

ALLOWED_EXTENSIONS = ['.jpg','.png','.gif']

#检查文件是否允许上传
def allowed_file(filename):
    _,ext = os.path.splitext(filename)
    #拆分扩展名，只获取后半部分ext = os.path.splitext(filename)[1]
    return ext.lower() in ALLOWED_EXTENSIONS    #返回True或False

#呈现特定目录下的资源
@back.route('/profile/<filename>/')
def render_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@back.route('/feedback/')
def feedback():
    items = db.session.query(Category).all()
    return render_template('post.html',items = items)

@back.route('/post_feedback/',methods=['POST'])
def post_feedback():
    if request.method == 'POST':
        feedback = Feedback(
            Subject = request.form['subject'],
            Username = request.form.get('username'),
            Email = request.form.get('email'),
            Image = None,
            Body = request.form.get('body'),
            State = request.form.get('state',0),
            Reply = request.form.get('reply'),
            ReleaseTime = datetime.now()
        )

        if 'screenshot' in request.files:
        # if request.files['screenshot',None]:
            img = request.files['screenshot']
            if img and allowed_file(img.filename):
                img_path = datetime.now().strftime('%Y%m%d%H%M%f') + os.path.splitext(img.filename)[1]
                feedback.Image = img_path
                img.save(os.path.join(UPLOAD_FOLDER,img_path))

        feedback.CategoryID = int(request.form.get('classify'))
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('back.feedback'))

@back.route('/admin/list/')
def feedback_list():
    if session.get('admin', None) is None:
        return redirect(url_for('admin.sign'))

    else:
        key = request.args.get('key', '')
        items = db.session.query(Feedback).filter(Feedback.Subject.contains(key)).all()
        return render_template('feedback-list.html',items=items)

@back.route('/admin/edit/<id>/')
def edit_feedback(id):
    if session.get('admin', None) is None:
        return redirect(url_for('admin.sign'))
    else:
        items = db.session.query(Category).all()
        current_feedback = db.session.query(Feedback).get(id)
        return render_template('edit.html',current_feedback = current_feedback,items=items)

@back.route('/admin/save_edit/',methods=['POST'])
def save_feedback():
    if request.method == 'POST':
        username = request.form.get('username')
        feed = db.session.query(Feedback).filter(Feedback.Username == username).first()

        feed.Subject = request.form['subject']
        feed.Username = request.form['username']
        feed.CategoryID = int(request.form.get('classify'))
        feed.Email = request.form.get('email')
        feed.Body = request.form.get('body')
        feed.State = 1 if request.form.get('state') == 'on' else 0
        feed.Reply = request.form.get('reply')
        feed.ReleaseTime = datetime.strptime(request.form.get('releasetime'),'%Y-%m-%d %H:%M:%S')
        db.session.commit()
        #图片存储的地址不用修改，所以不用写
        #request.form.get()得到的数据类型都是字符串，需用datetime.strptime()转换成datetime类型
        #查询时，filter()条件后要加.first()
    return redirect(url_for('back.feedback_list'))

@back.route('/admin/feedback/del/<id>/')
def delete_feedback(id):
    back = db.session.query(Feedback).get(id)
    db.session.delete(back)
    db.session.commit()
    return redirect(url_for('back.feedback_list'))
