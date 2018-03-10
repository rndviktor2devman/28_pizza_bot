from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


pizza_choice = db.Table(
    'pizza_choice',
    db.Column('pizza_id', db.Integer(), db.ForeignKey('pizza.id')),
    db.Column('choice_id', db.Integer(), db.ForeignKey('choice.id'))
)


class Pizza(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    choices = db.relationship('Choice', secondary=pizza_choice, backref=db.backref('pizza', lazy='dynamic'))

    def __repr__(self):
        return 'title=%s, description=%s' % (self.title, self.description)


class Choice(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    price = db.Column(db.Numeric)

    def __repr__(self):
        return 'title=%s, price=%s' % (self.title, self.price)


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.Unicode(128))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email
