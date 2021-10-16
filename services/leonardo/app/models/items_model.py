from django.db import models


class Item(models.Model):
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, related_name="items", null=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self.name=}, {self.category.name=})"
