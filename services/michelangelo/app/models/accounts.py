import datetime

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Account(models.Model):
    user = fields.ForeignKeyField("models.User", related_name="account")
    has_to_change_password = fields.BooleanField(default=False)
    password_changed_datetime = fields.DatetimeField(default=None)
    two_factor_auth = fields.BooleanField(default=False)
    account_token = fields.CharField(max_length=255, default=None, null=True)

    async def need_to_change_password(self):
        return (datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() > self.password_changed_datetime.timestamp()


Account_Pydantic = pydantic_model_creator(Account, name="Account")
