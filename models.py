from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_security import SQLAlchemyUserDatastore

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Pizza(db.Model):
    __tablename__ = 'pizza'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    choices = db.relationship("Choice", back_populates="pizza")

    def __repr__(self):
        return 'title=%s, description=%s' % (self.title, self.description)


class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    price = db.Column(db.Numeric)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    pizza = db.relationship("Pizza", back_populates="choices")

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
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
