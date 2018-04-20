from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from admin import admin as blueprint_admin

app = Flask(__name__,static_url_path='')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/personal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'fdkhafhkda'


db = SQLAlchemy(app)

from personal import employee
app.register_blueprint(employee,url_prefix='/admin')
app.register_blueprint(blueprint_admin,url_prefix='/admin')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/admin/')
def admin_index():
    return render_template('admin/layout.html')

# @app.route('/admin/emp/list/')
# def admin_emp_list():
#     from personal import Employee
#     items = db.session.query(Employee).limit(10)
#     return render_template('admin/emp-list.html', items=items)

if __name__ == '__main__':
    app.run()
