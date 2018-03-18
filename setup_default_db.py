from models import Base, engine, session, Pizza, Choice, Role, user_datastore, db
import json
import argparse
import os
from werkzeug.security import generate_password_hash


def get_catalog_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('catalog_path', help='Mandatory parameter')
    return parser.parse_args()


def get_json_data_from_file(meals_catalog_path):
    if not os.path.exists(meals_catalog_path):
        return None
    with open(meals_catalog_path, 'r') as meals_catalog:
        return json.loads(meals_catalog.read())


def push_to_db(items):
    db.drop_all()
    db.create_all()
    for item in items:
        pizza = Pizza(title=item['title'], description=item['description'])
        session.add(pizza)
        for choise in item['choices']:
            option = Choice(title=choise['title'], price=choise['price'])
            pizza.choices.append(option)
        session.add(pizza)
    session.commit()

    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()
    user_datastore.create_user(
        login='admin',
        password=generate_password_hash('123456'),
        roles=[user_role, super_user_role]
    )
    db.session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    pizza_catalog = get_catalog_path()
    pizzas = get_json_data_from_file(pizza_catalog.catalog_path)
    push_to_db(pizzas)
