# Telegram Bot for Pizzeria

The project is simple example of Pizzeria telegram bot and it's Admin Panel

## Features
* Items catalog is stored in mysql db
* Admin is able to edit products list on Admin Pane

## Usage
1. Set up required packages
2. Setup default database(created admin user(admin-123456) and data catalog)
3. If needed, edit the pizzas list
4. Retrieve token from bot father and add it to local environment variables
5. Run the bot application

Example of run on Python3:
```
pip3 install -r requirements
python3 setup_default_db.py catalog_data.json
export BOT_TOKEN="token retrieved from bot father"
python3 bot.py
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
