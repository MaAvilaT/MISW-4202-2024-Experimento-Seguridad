from fastapi import FastAPI, HTTPException, status, Depends
from database import engine, yield_db_session

import models

from typing import Annotated
from sqlalchemy.orm import Session

from authentication import router

app = FastAPI()
app.include_router(router)

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(yield_db_session)]


@app.get("/authentication")
async def user(user: None | dict, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication credentials were not provided'
        )

    return {'user': user}
