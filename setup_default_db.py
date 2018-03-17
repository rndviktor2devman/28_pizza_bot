from models import Base, engine, session, Pizza, Choice
import json
import argparse
import os


def get_meals_catalog_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('meals_catalog_path', help='Mandatory parametr')
    return parser.parse_args()


def load_meals_catalog_from_file(meals_catalog_path):
    if not os.path.exists(meals_catalog_path):
        return None
    with open(meals_catalog_path, 'r') as meals_catalog:
        return json.loads(meals_catalog.read())


def insert_into_db(items):
    for item in items:
        pizza = Pizza(title=item['title'], description=item['description'])
        session.add(pizza)
        for choise in item['choices']:
            option = Choice(title=choise['title'], price=choise['price'])
            pizza.choices.append(option)
        session.add(pizza)
    session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    meals_catalog = get_meals_catalog_path()
    meals = load_meals_catalog_from_file(meals_catalog.meals_catalog_path)
insert_into_db(meals)