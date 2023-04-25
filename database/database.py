
import databases

import os


from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(ROOT_DIR, '.env'))


SQL=os.getenv('SQL')
SQL_USER=os.getenv('SQL_USER')
SQL_PASS=os.getenv('SQL_PASS')
SQL_HOST=os.getenv('SQL_HOST')
SQL_DATABASE=os.getenv('SQL_DATABASE')

SQLITE_DATABASE_URL=F"{SQL}://{SQL_USER}:{SQL_PASS}@{SQL_HOST}/{SQL_DATABASE}?charset=utf8mb4"

engine = create_engine(
    SQLITE_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()