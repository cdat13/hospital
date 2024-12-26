
from app import app, db
from flask_admin import Admin, BaseView, expose
from app.models import User, Appointment, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect


admin = Admin(app=app, name="Quản lý hệ thống bệnh viện", template_mode="bootstrap4")



class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html', cates=dao.stats_products())


class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(MyView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')



class AppointView(AuthenticatedView):
    can_view_details = True
    can_export = True
    # column_searchable_list = ['date']


admin.add_view(AuthenticatedView(User, db.session))
admin.add_view(AppointView(Appointment, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))


