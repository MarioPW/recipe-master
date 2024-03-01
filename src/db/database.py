from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, declarative_base 
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv("DB_URL")

try:
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
except Exception as e:
    print(f'Error in database connection: {e}')
finally:
    session.close()

