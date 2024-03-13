import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .constants import TOKEN_VALIDITY_IN_MINUTES, ALGORITHM, SECRET_KEY
from .database import yield_db_session
from .models import User, UserRole

router = APIRouter(
    prefix='/authentication',
    tags=['Authentication']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='authentication/token')


class CreateUserRequest(BaseModel):
    username: str
    password: str
    type: UserRole
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


db_dependency = Annotated[Session, Depends(yield_db_session)]


@router.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest) -> dict:
    existing_user = db.query(User).filter(or_(User.username == request.username,
                                              User.email == request.email)).first()

    if existing_user:
        match existing_user.username:
            case request.username:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail='Username already exists')
            case request.email:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail='Email already exists')

    create_user_model = User(
        username=request.username,
        type=request.type,
        hashed_password=bcrypt_context.hash(request.password),
        email=request.email,
    )

    db.add(create_user_model)
    db.commit()

    return {
        'username': request.username,
        'user_type': request.type,
    }


@router.post('/token', response_model=Token)
async def access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       db: db_dependency) -> dict:
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect data')

    encode: dict = {
        'sub': user.username,
        'id': str(user.user_id),
        'exp': datetime.datetime.now(datetime.UTC) + timedelta(minutes=TOKEN_VALIDITY_IN_MINUTES)
    }

    return {
        'access_token': jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM),
        'token_type': 'bearer'
    }


async def decode_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not payload.get('sub') or not payload.get('id'):
            raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST,
                                detail='Unable to validate credentials')

        return payload.get('sub')

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized credentials')
