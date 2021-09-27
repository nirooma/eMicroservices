from tortoise import fields, models
from tortoise.manager import Manager


# class UserManager(Manager):
#     def get_queryset(self):
#         return super().get_queryset()
#
#     def get_latest_5_objects(self):
#         return super(UserManager, self).get_queryset().limit(5)


class User(models.Model):
    username = fields.CharField(max_length=255, unique=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    email = fields.CharField(max_length=255, null=True, default=None, unique=True)
    password = fields.CharField(max_length=255, null=False)
    phone = fields.CharField(max_length=30, unique=True)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)

    # objects = UserManager()

    class Meta:
        ordering = ["-id"]