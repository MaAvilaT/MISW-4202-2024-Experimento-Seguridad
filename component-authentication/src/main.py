from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

from . import constants
from . import models
from .database import engine, yield_db_session
from .authentication import router, decode_current_user
from .models import User


app = FastAPI()
app.include_router(router)

origins = [
    constants.COMPONENT_AUTHORIZATION_BASE_URL,
    constants.COMPONENT_AUTHENTICATION_BASE_URL,
    constants.COMPONENT_API_GATEWAY_BASE_URL,
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.get('/authenticate', status_code=status.HTTP_200_OK)
async def authenticate(username: Annotated[dict, Depends(decode_current_user)],
                       db: Annotated[Session, Depends(yield_db_session)]):
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication credentials were not provided'
        )

    user = db.query(User).filter(User.username == username).one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )

    return {
        'username': username,
        'role': user.role,
    }
