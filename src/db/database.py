from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, declarative_base 
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = getenv("DB_URL")

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
except ValueError as e:
    print(f'Error in database connection: {e}')
finally:
    session.close()
