from typing import Annotated

import uvicorn
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.models import User
from . import constants
from . import models
from .authentication import router, decode_current_user
from .database import engine, yield_db_session

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
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User is suspended'
        )

    return {
        'username': username,
        'role': user.role,
    }


if __name__ == "__main__":
    uvicorn.run(app='src.main:app', host="0.0.0.0", port=9393, log_level='debug', reload=True)
