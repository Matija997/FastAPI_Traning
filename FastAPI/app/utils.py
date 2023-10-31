from passlib.context import CryptContext

pwd_contex= CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_contex.hash(password)

def verify(plain_password,hashed_pasword):
    return pwd_contex.verify(plain_password,hashed_pasword)