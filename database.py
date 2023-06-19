from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    name = Column(String(50))
    email = Column(String(50))
    card_number = Column(String(20))
    password = Column(String(100))


class Database:
    def __init__(self, host, user, password, database):
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
        self.Session = sessionmaker(bind=self.engine)

    def insert_user(self, name, email, username, card_number, password):
        session = self.Session()
        user = User(name=name, email=email, username=username, card_number=card_number, password=password)
        session.add(user)
        session.commit()
        session.close()

    def get_user_by_username(self, username):
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        return user
