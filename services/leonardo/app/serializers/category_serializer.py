from rest_framework.serializers import ModelSerializer

from app.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ["id", "name", "is_active"]
        model = Category
