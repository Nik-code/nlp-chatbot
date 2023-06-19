from main import db
import bcrypt


def insert_user(name, email, username, card_number, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.insert_user(name, email, username, card_number, hashed_password)


def get_user_by_username(username):
    return db.get_user_by_username(username)
