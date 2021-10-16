from rest_framework.serializers import ModelSerializer

from app.models import Item


class ItemSerializer(ModelSerializer):
    class Meta:
        fields = ["id", "name", "created_at"]
        model = Item
