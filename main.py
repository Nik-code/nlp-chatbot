from flask import Flask
import os
import dotenv
import database

dotenv.load_dotenv('values.env')

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
# Initialize the database
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
db = database.Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)


if __name__ == '__main__':
    app.run(debug=True, port=6000)
