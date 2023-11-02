from typing import Optional,List
from fastapi import Body, FastAPI, Response, status,HTTPException, Depends,APIRouter

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,oauth2



router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)




@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
              limit: int = 10 , skip: int = 0, search: Optional[str] = ""):
    #WITH SQL WE USE THIS  
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()

    #SQLAlchemy
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    #SQL
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)  RETURNING *""",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
   
    #SQLAlchemy
    print(current_user.email)
    new_post=models.Post(**post.dict())
    new_post.owner_id=current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest",response_model=schemas.Post)
def get_latest_post(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).order_by(models.Post.id.desc()).first()
   
    return post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    #SQL
    #cursor.execute("""SELECT * from posts WHERE id=%s""",(str(id)))
    # post=cursor.fetchone()

    #SQLAlchemy
    post= db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #SQL
    #cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    #SQLAlchemy
    post=db.query(models.Post).filter(models.Post.id==id)
   
    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    #SQL
    #cursor.execute("""UPDATE posts SET title= %s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()

    #SQLAlchemy
    updated_post=db.query(models.Post).filter(models.Post.id==id)
    if updated_post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()
   
    return updated_post.first()
