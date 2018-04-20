from flask import Blueprint

admin = Blueprint('admin',__name__)

from admin.views import *

emp_list_view = EmployeeListView.as_view('emp_list')

admin.add_url_rule('/emp/list/',view_func=emp_list_view)
admin.add_url_rule('/emp/list/<int:page>/',view_func=emp_list_view)


admin.add_url_rule('/emp/del/<id>/',view_func=EmployeeDelView.as_view('emp_del'))

admin.add_url_rule('/emp/create/',view_func=EmployeeCreateOrEdit.as_view('emp_create'))
admin.add_url_rule('/emp/edit/<id>',view_func=EmployeeCreateOrEdit.as_view('emp_edit'))


