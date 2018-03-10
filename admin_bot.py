from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin.form import rules
from flask_security.utils import encrypt_password
import os
from models import app, User, Role, db, Pizza, Choice



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class MyViewModel(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    edit_template = 'rule_edit.html'


@app.route('/')
def index():
    return render_template('index.html')


admin = flask_admin.Admin(
    app,
    'Pizza bot Admin',
    base_template='my_master.html',
    template_mode='bootstrap3'
)

# admin.add_view(MyViewModel(Role, db.session))
# admin.add_view(MyViewModel(User, db.session))
admin.add_view(MyViewModel(Pizza, db.session))
admin.add_view(MyViewModel(Choice, db.session))


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


def build_sample_db():
    """
    Populate a small db with some example entries.
    """
    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        user_datastore.create_user(
            login='Admin',
            email='admin',
            password=encrypt_password('123456'),
            roles=[user_role, super_user_role]
        )
        db.session.commit()
    return


if __name__ == '__main__':
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    app.run(debug=True)
