from flask import url_for, redirect, render_template, request, Response, abort
import flask_admin as fla
from flask_admin.contrib import sqla
import os
from models import app, db, Pizza, Choice
from flask_admin.form import RenderTemplateWidget
from flask_admin.contrib.sqla.fields import InlineModelFormList
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.model.form import InlineFormAdmin
from werkzeug.exceptions import HTTPException


class CustomInlineFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super(CustomInlineFieldListWidget, self).__init__('field_list.html')


class CustomInlineModelFormList(InlineModelFormList):
    widget = CustomInlineFieldListWidget()

    def display_row_controls(self, field):
        return False


class CustomInlineModelConverter(InlineModelConverter):
    inline_field_list_type = CustomInlineModelFormList


class InlineModelForm(InlineFormAdmin):
    form_label = 'Choice'

    def __init__(self):
        return super(InlineModelForm, self).__init__(Choice)


class AuthException(HTTPException):

    def __init__(self, message):

        super().__init__(
            message, Response(

                "You could not be authenticated. Please refresh the page.", status=401,
                headers={'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        )


class MyViewModel(sqla.ModelView):
    inline_model_form_converter = CustomInlineModelConverter

    inline_models = (InlineModelForm(),)

    def __init__(self):
        super(MyViewModel, self).__init__(Pizza, db.session, name='Pizzas')

    @staticmethod
    def check_auth(username, password):
        return username == os.getenv('USERNAME') and \
               password == os.getenv('PASSWORD')

    def is_accessible(self):
        auth = request.authorization
        if not auth or not self.check_auth(auth.username, auth.password):
            raise AuthException('Not authenticated')

        return True


@app.route('/')
def index():
    pizzas = db.session.query(Pizza).all()
    return render_template('index.html', pizzas=pizzas)


admin = fla.Admin(app, 'Bot Admin App')
admin.add_view(MyViewModel())


if __name__ == '__main__':
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        raise Exception('the database was not created')

    app.run(debug=True)
