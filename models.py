from sqlalchemy import Column, String, Integer
from database import base

class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50))
    second_name = Column(String(50))


class Record(base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String(50), unique=True)
    content = Column(String(255))
    user_id = Column(Integer)

    