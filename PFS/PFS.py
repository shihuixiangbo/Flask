from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key="khhskdhskhds"

db = SQLAlchemy(app)

from feedback.models import Category,Feedback


from feedback import back
app.register_blueprint(back)

from login import admin
app.register_blueprint(admin)

@app.route('/')
def hello_world():
    return render_template('base.html')

if __name__ == '__main__':
    app.run()
