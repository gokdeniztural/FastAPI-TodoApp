from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:REDACTED@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Uygulamanın veritabanıyla etkileşimini sağlayan motor.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()