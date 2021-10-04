from typing import Dict
from fastapi import Depends, APIRouter, status, HTTPException, BackgroundTasks
from app.schemas.users import UserIn_Pydantic
import logging
from app.core import security
from app.crud import users
from app.core.jwt import create_access_token
from app.schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.configuration_utils import config
from app.utils import response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserIn_Pydantic, background_tasks: BackgroundTasks):
    credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=config.get("errors")["loginError"]
        )
    user = await users.create_user(payload)
    if not user:
        raise credentials_exception
    await user.send_mail(
        "welcome_email",
        task_details={"first_name": user.first_name, "last_name": user.last_name},
        background_tasks=background_tasks
    )
    logger.info(f"new account added to the dibi {user.email=}")
    return response(detail=config.get("defaultAnswer"), status_code=status.HTTP_201_CREATED)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_payload: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=config.get("errors")["loginError"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await security.authenticate(form_payload.username, form_payload.password)
    if not user or user.is_active is False:
        raise credentials_exception
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "phone": user.phone}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/forgot_password', status_code=status.HTTP_200_OK)
async def reset_password(email: str, background_tasks: BackgroundTasks) -> Dict:
    if user := await users.get_user_by_email(email):
        token = await user.generate_token()
        await user.send_mail(
            task_name="reset_password",
            task_details={"token": token},
            background_tasks=background_tasks
        )
        logger.info(f"reset password has been send to the email {email!r}")

    return response(config.get("errors")["forgotPassword"])

