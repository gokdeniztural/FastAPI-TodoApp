from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:REDACTED@localhost/TodoApplicationDatabase'

#engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Uygulamanın veritabanıyla etkileşimini sağlayan motor.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # test_todos.py dosyasında da kullanmak için Base'i burada tanımlıyoruz.