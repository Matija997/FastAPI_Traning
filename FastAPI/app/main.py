from typing import Optional,List
from fastapi import Body, FastAPI, Response, status,HTTPException, Depends
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine,get_db
from . import models,schemas,utils
from .routers import posts,users,auth


models.Base.metadata.create_all(bind=engine)

app= FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


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

#my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
        #  {"title":"favorite foods","content":"I like pizza","id":2}]

#def find_post(id):
  #  for p in my_posts:
   #     if p["id"]==id:
    #        return p

#def find_index_post(id):
    #for i, p in enumerate(my_posts):
      #  if p['id']==id:
        #    return i
        

@app.get("/")
def root():

    return {"message": "Hello World !!!"}




