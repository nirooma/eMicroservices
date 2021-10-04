import datetime
from fastapi import BackgroundTasks, Depends
from tortoise import fields, models
from app import consts
from app.core.jwt import create_access_token
from typing import List, Dict

from tortoise.signals import post_save
import logging

from app.core.queue import send_task_to_queue

logger = logging.getLogger(__name__)


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    email = fields.CharField(max_length=255, null=True, default=None, unique=True)
    first_name = fields.CharField(max_length=255, null=True, default="")
    last_name = fields.CharField(max_length=255, null=True, default="")
    password = fields.CharField(max_length=255, null=False)
    phone = fields.CharField(max_length=30, unique=True, null=True)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"<{self.__class__.__name__}({self.id}, {self.username})>"

    async def generate_token(self) -> str:
        return create_access_token(
            data={"username": self.username},
            expires_delta=datetime.timedelta(days=consts.DEFAULT_DAYS_RESET_PASSWORD),
            general_use=True
        )

    async def send_mail(self, task_name: str, *, task_details: Dict, background_tasks: BackgroundTasks):
        background_tasks.add_task(
            send_task_to_queue,
            task_name=f"send_mail.{task_name}",
            task_details={"username": self.username, "email": self.email, **task_details},
        )


@post_save(User)
async def post_save_signal(
        sender: "Type[User]",
        instance: User,
        created: bool,
        using_db: "Optional[BaseDBAsyncClient]",
        update_fields: List[str]
):
    """ Create an account for a new user """
    from app.models import Account
    if created:
        await Account.create(
            user=instance, has_to_change_password=False, password_changed_datetime=datetime.datetime.now()
        )
        logger.info(f"account has been created for user {instance.username!r}")



