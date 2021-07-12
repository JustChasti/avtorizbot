import sys
import os
import psycopg2
from datetime import datetime, timedelta

import config
import createbase

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    send_count = Column(Integer, nullable=False)
    name = Column(String(256), nullable=False)
    curretn_email = Column(String(256), nullable=False)
    curretn_code = Column(String(256), nullable=False)
    code_time = Column(DateTime(timezone=False), default=datetime.now())
    get_count = Column(Integer, nullable=True)


user = config.base_user
passs = config.base_pass
name = config.base_name


try:
    engine = create_engine("postgresql+psycopg2://" + user + ":" + passs + "@localhost/" + name)
    engine.connect()
except Exception as e:
    createbase.create(user, passs, name)
    engine = create_engine("postgresql+psycopg2://" + user + ":" + passs + "@localhost/" + name)
    engine.connect()
Base.metadata.create_all(engine)
Base.metadata.bind = engine


Session = sessionmaker(bind=engine)


def find_user(name):
    session = Session()
    try:
        u = session.query(User).filter(User.name == name).one()
        return u.send_count
    except Exception as e:
        return 'this profile isnt in database'


def get_email(name):
    session = Session()
    try:
        u = session.query(User).filter(User.name == name).one()
        return u.curretn_email
    except Exception as e:
        return 'this profile isnt in database'


def add_user(name, email, code):
    session = Session()
    try:
        user = User(name=name, send_count=1, curretn_email=email, curretn_code=code, code_time=datetime.now(), get_count=0)
        session.add(user)
        session.commit()
    except Exception as e:
        print('создание пользователя не удалось')
    session.close()


def change_email(name, email, code):
    session = Session()
    upd = session.query(User).filter(User.name == name).one()
    upd.send_count += 1
    upd.curretn_email = email
    upd.curretn_code = code
    upd.get_count = 0
    upd.code_time=datetime.now()
    session.commit()
    session.close()


def change_code(name, code):
    session = Session()
    upd = session.query(User).filter(User.name == name).one()
    upd.curretn_code = code
    upd.send_count += 1
    upd.get_count = 0
    upd.code_time=datetime.now()
    session.commit()
    session.close()


def get_code(name):
    session = Session()
    user = session.query(User).filter(User.name == name).one()
    user.get_count += 1
    if user.get_count >= 15:
        session.commit()
        session.close()
        return 'to many attempts'
    d = datetime.now() - timedelta(hours=config.hours)
    if user.code_time >= d:
        c = user.curretn_code
        session.commit()
        session.close()
        return c
    else:
        session.commit()
        session.close()
        return 'time is over'


if __name__ == "__main__":
    print(get_code('test1'))
