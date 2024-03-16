import json
import logging

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from . import constants
from .authorization import router, RequestDTO

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
    allow_methods=['*'],
    allow_headers=['*'],
)

logger = logging.getLogger(constants.LOGGER_NAME)


@app.post('/authorize', status_code=status.HTTP_200_OK)
async def check_accesses(request_dto: RequestDTO, server_response: Response):
    """
    Checks access to the requested endpoint by requiring a mandatory access token.
    Then if component authentication confirms, we can proceed with the checking of access from the user.

    Taking in consideration that /authenticate endpoint returns the role of the user, we can
    give more credibility to the action it wants to execute.

    :param server_response: this server's response.
    :param request_dto: the request data, includes:
    - "token": the access token.
    - "request": an arbitrary dictionary containing an endpoint and further data to feed the endpoint.
    :return: `status.HTTP_200_OK` if the request is valid, otherwise `status.HTTP_401_UNAUTHORIZED`.
    """
    response = requests.get(f'{constants.COMPONENT_AUTHENTICATION_BASE_URL}/authenticate',
                            headers={'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {request_dto.token["access_token"]}'})

    if response.status_code != 200:
        logger.log(level=logging.CRITICAL, msg=f'External request with token `{request_dto.token["access_token"]}` '
                                               f'has attempted an unauthorized request to '
                                               f'`{request_dto.request["endpoint"]}` endpoint'
                                               f'with details `{json.dumps(request_dto.request)}`')

        raise HTTPException(status_code=response.status_code,
                            detail=response.json())

    if request_dto.request['endpoint'] not in constants.RULES[response.json().get('role')]:
        logger.log(level=logging.WARN, msg=f'user with role `{response.json().get("role")}` '
                                           f'has attempted an unauthorized request to '
                                           f'`{request_dto.request["endpoint"]}` endpoint')

        # SUSPEND USER
        match response.json().get('role'):
            case constants.Role.SPORTSMAN:
                pass
            case constants.Role.ORG:
                pass
            case constants.Role.BUSINESS_PARTNER:
                pass

        requests.post(url=f'{constants.COMPONENT_AUTHENTICATION_BASE_URL}/authentication/suspend',
                      headers={'Content-Type': 'application/json',
                               'Authorization': f'Bearer {request_dto.token["access_token"]}'})

        server_response.status_code = status.HTTP_403_FORBIDDEN

        return {
            'action_authorized': False,
            'user_suspended': True,
        }

    return {
        'action_authorized': True
    }


if __name__ == "__main__":
    uvicorn.run(app='src.main:app', host='0.0.0.0', port=4343, log_level='debug', reload=True)
