from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    username: str
    password: str
    type: str
    email: str


class LoggedUserRequest(BaseModel):
    token: dict
    request: dict
