from app import db

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
    price = db.Column(db.Integer)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    pizza = db.relationship("Pizza", back_populates="choices")

    def __repr__(self):
        return 'title=%s, price=%s' % (self.title, self.price)
