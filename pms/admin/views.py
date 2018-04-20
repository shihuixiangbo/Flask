from flask import render_template,redirect,url_for,request
from flask.views import MethodView
from personal.models import *
from admin import admin
from personal.forms import EmployeeForm

class EmployeeListView(MethodView):
    def get(self,page=1):
        items = db.session.query(Employee).paginate(page,per_page=10)
        return render_template('admin/emp-list.html', items=items)

class EmployeeDelView(MethodView):
    def get(self,id=None):
        if id:
            emp = db.session.query(Employee).get(id)
            if emp:
                db.session.delete(emp)
                db.session.commit()
        return redirect(url_for('admin.emp_list'))

class EmployeeCreateView(MethodView):
    def get(self):
        deps = db.session.query(Department).all()
        return render_template('admin/emp-detail.html',deps = deps)

    def post(self):
        employee = Employee(
            request.form.get('name'),
            request.form.get('gender'),
            request.form.get('job'),
            datetime.strptime(request.form.get('birthdate'),'%Y-%m-%d'),
            request.form.get('idcard'),
            request.form.get('address'),
            float(request.form.get('salary'))
        )

        employee.department_id = int(request.form.get('department_id'))

        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('admin.emp_list'))

# class EmployeeCreateOrEdit(MethodView):
#     def get(self,id=None):
#         form = EmployeeForm()
#         form.department_id.choices = [(d.id, d.name) for d in db.session.query(Department).all()]
#         return render_template('admin/emp-edit.html',form=form)
#
#     def post(self):
#         form = EmployeeForm(request.form)
#         emp = Employee(
#             form.name.data,
#             form.gender.data,
#             form.job.data,
#             form.birthdate.data,
#             form.idcard.data,
#             form.address.data,
#             form.salary.data
#         )
#         emp.department_id = form.department_id.data
#         db.session.add(emp)
#         db.session.commit()
#
#         return redirect(url_for('admin.emp_list'))

#简化操作

class EmployeeCreateOrEdit(MethodView):
    def get(self,id=None):
        emp = Employee() if not id else db.session.query(Employee).get(id)
        form = EmployeeForm(request.form,obj=emp)
        #将emp的数据塞给form

        form.department_id.choices = [(d.id, d.name) for d in db.session.query(Department).all()]
        return render_template('admin/emp-edit.html',form=form)

    def post(self,id=None):
        form = EmployeeForm(request.form)
        emp = Employee() if not id else db.session.query(Employee).get(id)
        #没有id就创建新的员工，否则就将旧的找出来

        form.populate_obj(emp)
        emp.department_id = form.department_id.data

        if not id:
            db.session.add(emp)
        db.session.commit()

        return redirect(url_for('admin.emp_list'))










