from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {self.is_active})"
