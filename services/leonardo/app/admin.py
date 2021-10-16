from django.contrib import admin

from app.models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["id", "name", "is_active"]
    readonly_fields = ["id"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ["id", "category", "name", "created_at"]
    readonly_fields = ["id", "created_at"]
