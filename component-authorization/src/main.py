from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests

from .authorization import router, UserDTO
from . import constants

app = FastAPI()

if __name__ == "__main__":
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
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.get('/authorize')
async def check_accesses(user: UserDTO):
    response = requests.post(constants.COMPONENT_AUTHENTICATION_BASE_URL, json={
        'username': user.username,
        'password': user.password
    })

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.json())

    return {
        'user': user
    }
