from tortoise import fields, models
from tortoise.manager import Manager
from tortoise.contrib.pydantic import pydantic_model_creator

# class UserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset()
#
#     def get_latest_5_objects(self):
#         return super(UserManager, self).get_queryset().limit(5)


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

    # objects = UserManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"<{self.__class__.__name__}({self.id}, {self.username})>"


User_Pydantic = pydantic_model_creator(User, name="User", exclude=["password"])
UserIn_Pydantic = pydantic_model_creator(
    User,
    name="UserIn",
    exclude_readonly=True,
    exclude=["is_active", "is_superuser", "is_staff"]
)
