import logging
from typing import Dict
from fastapi import Depends, APIRouter, status, HTTPException, BackgroundTasks, Request
from starlette.authentication import requires
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from tortoise.transactions import atomic

from app.consts import DEFAULT_COOKIE_TTL
from app.crud.users import create_system_user
from app.models import Account
from app.schemas.users import UserIn_Pydantic
from app.core import security
from app.crud import users
from app.core.jwt import create_access_token
from app.schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.configuration_utils import config
from app.utils import _response, decode_base64

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
@atomic()
async def register(payload: UserIn_Pydantic, background_tasks: BackgroundTasks):
    credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=config.get("errors")["loginError"]
        )
    user = await users.create_user(payload)
    await create_system_user()
    if not user:
        raise credentials_exception
    token = await user.generate_token()
    await user.send_mail(
        "welcome_email",
        task_details={"first_name": user.first_name, "last_name": user.last_name, "token": token},
        background_tasks=background_tasks
    )
    logger.info(f"New account added to the dibi {user.email=}")
    return _response(detail=config.get("defaultAnswer"), status_code=status.HTTP_201_CREATED)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(response: Response, form_payload: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=config.get("errors")["loginError"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await security.authenticate(form_payload.username, form_payload.password)
    if not user or not user.is_active:
        logger.error(f"User {form_payload.username!r} failed to connect")
        raise credentials_exception
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "phone": user.phone}
    )
    response.set_cookie("SessionToken", access_token, httponly=True, max_age=DEFAULT_COOKIE_TTL)
    logger.info(f"Cookie set for user {user.username!r}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/logout')
@requires(['authenticated'])
async def logout(request: Request, response: Response):
    response.delete_cookie("SessionToken")
    return _response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/forgot_password', status_code=status.HTTP_200_OK)
@atomic()
async def reset_password(email: str, background_tasks: BackgroundTasks) -> Dict:
    if user := await users.get_user_by_email(email):
        user_account: Account = await user.user_account
        token = await user.generate_token()
        # send task to the queue
        await user.send_mail(
            task_name="reset_password",
            task_details={"token": token},  # TODO: Remove
            background_tasks=background_tasks
        )
        logger.info(f"reset password has been send to the email {email!r}")
        user_account.has_to_change_password = True
        await user_account.save()

    return _response(config.get("errors")["forgotPassword"])


@router.get('/account_confirmation')
async def account_confirmation(token: str, request: Request):
    try:
        decode_token = decode_base64(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=config.get("errors")["tokenError"]
        )

    user = await users.get_user_by_username(decode_token["username"])
    # Account already activated.
    if user.is_active:
        return _response(detail=config.get("errors")["activeAccount"])

    user.is_active = True
    await user.save()
    logger.info(f"Account activated for user {user.username!r}")
    return templates.TemplateResponse(
        "account_confirmation.html",
        context={"request": request, "user": user}
    )
