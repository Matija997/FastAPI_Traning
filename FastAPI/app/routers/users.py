
from fastapi import Body, FastAPI, Response, status,HTTPException, Depends,APIRouter

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/")
def get_users(db:Session=Depends(get_db)):

    users=db.query(models.User).all()

    return {"data":users}


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):

    
    user.password=utils.hash(user.password)

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return user