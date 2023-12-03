import pydantic


class TokenResponse(pydantic.BaseModel):
    access_token: str
    token_type: str


class CurrentUserResponse(pydantic.BaseModel):
    name: str
    email: str
