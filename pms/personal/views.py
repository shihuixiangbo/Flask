from datetime import datetime


from flask import render_template
from flask.views import MethodView

from pms import db
from personal import employee
from .models import Employee,Department

class EmployeeListView(MethodView):
    def get(self):
        employees = db.session.query(Employee).all()[:10]
        return render_template('employee-list.html',employees = employees)

employee.add_url_rule('/list/',view_func=EmployeeListView.as_view('emp_list'))


