from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

#CONNECTING WITH DATABASE USING SQLALCHEMY
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessinoLocal= sessionmaker(autocommit=False, autoflush=False,bind=engine)


Base= declarative_base()

def get_db():
    db=SessinoLocal()
    try:
        yield db
    finally:
        db.close()

#CONNECTING WITH DATABASE USING PSYCOPG2
#while True:
  #  try:
   #     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='tdiradio',cursor_factory=RealDictCursor)
     #   cursor=  conn.cursor()
   #     print("Connection with database was succesfull")
  #      break
   # except Exception as error:
    #    print("Connection failed")
     #   print("Error: ",error)
      #  time.sleep(2)  
