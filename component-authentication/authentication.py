import os
from datetime import timedelta
import datetime
from typing import Generator, Annotated

from sqlalchemy.orm import Session
from database import SessionLocal, yield_db_session
from models import User

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError


router = APIRouter(
    prefix='/authentication',
    tags=['Authentication']
)


ENV_SECRET = os.environ.get('ENV_SECRET_KEY')

SECRET_KEY = ENV_SECRET if ENV_SECRET else 'TRDYJH8587TYFKG%$^&%HJB<8759YGKJH<*O:YUILH>KJ'
ALGORITHM = 'HS256'

TOKEN_VALIDITY_MINUTES = 20


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


db_dependency = Annotated[Session, Depends(yield_db_session)]


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    create_user_model = User(
        username=request.username,
        hashed_password=bcrypt_context.hash(request.password),
        email=request.email,
    )

    db.add(create_user_model)
    db.commit()

    return {
        'username': request.username,
    }


@router.post("/token", response_model=Token)
async def access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       db: db_dependency):

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect data')

    encode: dict = {
        'sub': user.username,
        'id': str(user.user_id),
        'exp': datetime.datetime.now(datetime.UTC) + timedelta(minutes=TOKEN_VALIDITY_MINUTES)
    }

    return {
        'access_token': jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM),
        'token_type': 'bearer'
    }
