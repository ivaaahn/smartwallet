from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .entities import AccessTokenPayloadDC
from .errors import AccessTokenError, IncorrectPasswordError, UserNotFoundError
from .schemas import CurrentUserResponse, TokenResponse
from .services import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/tokens/access")


def check_auth(
    svc: AuthService = Depends(), token: str = Depends(oauth2_scheme)
) -> AccessTokenPayloadDC:
    try:
        return svc.token_handler.decode(token)
    except AccessTokenError as err:
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials",
        ) from err


@auth_router.post("/tokens/access")
async def get_token(
    svc: AuthService = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    try:
        token = await svc.login(
            email=form_data.username,
            password=form_data.password,
        )
    except (UserNotFoundError, IncorrectPasswordError) as err:
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials",
        ) from err

    return TokenResponse(
        access_token=token.access_token, token_type=token.token_type
    )


@auth_router.get("/me")
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    svc: AuthService = Depends(),
) -> CurrentUserResponse:
    try:
        current_user = await svc.get_current_user(token)
    except (UserNotFoundError, AccessTokenError) as err:
        raise HTTPException(
            status_code=401,
            detail="Access token not valid",
        ) from err

    return CurrentUserResponse(
        name=current_user.name,
        email=current_user.email,
    )
