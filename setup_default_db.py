from app import db, session, Base, engine
from models import Pizza, Choice
import json
import argparse
import os


def get_catalog_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('catalog_path', help='Mandatory parameter')
    return parser.parse_args()


def get_json_data_from_file(meals_catalog_path):
    if not os.path.exists(meals_catalog_path):
        return None
    with open(meals_catalog_path, 'r') as meals_catalog:
        return json.loads(meals_catalog.read())


def push_to_db(product_items):
    db.drop_all()
    db.create_all()
    for product_item in product_items:
        pizza = Pizza(title=product_item['title'],
                      description=product_item['description'])
        session.add(pizza)
        for choice in product_item['choices']:
            option = Choice(title=choice['title'], price=choice['price'])
            pizza.choices.append(option)
        session.add(pizza)
    session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    pizza_catalog = get_catalog_path()
    pizzas = get_json_data_from_file(pizza_catalog.catalog_path)
    push_to_db(pizzas)
