from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:tdiradio@localhost/fastapi'


engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessinoLocal= sessionmaker(autocommit=False, autoflush=False,bind=engine)


Base= declarative_base()

def get_db():
    db=SessinoLocal()
    try:
        yield db
    finally:
        db.close()