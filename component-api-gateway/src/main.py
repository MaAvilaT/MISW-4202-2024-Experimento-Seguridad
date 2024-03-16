import logging

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .models import RegisterUserRequest
from .sportsman_gateway import router as sportsman_router
from .org_gateway import router as org_router
from .partner_gateway import router as partner_router
from . import constants

app = FastAPI()

app.include_router(sportsman_router)
app.include_router(org_router)
app.include_router(partner_router)

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


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: RegisterUserRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='No user provided')

    response = requests.post(f'{constants.COMPONENT_AUTHENTICATION_BASE_URL}/authentication/user',
                             json=user.__dict__, headers={'Content-Type': 'application/json'})

    match response.status_code:
        case status.HTTP_422_UNPROCESSABLE_ENTITY:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Provided data is invalid')
        case status.HTTP_409_CONFLICT:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='User already exists')

    if response.status_code != status.HTTP_201_CREATED:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


if __name__ == "__main__":
    uvicorn.run(app='src.main:app', host="0.0.0.0", port=7373, log_level='debug', reload=True)
