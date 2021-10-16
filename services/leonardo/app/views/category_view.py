from typing import Dict, List, Any
from urllib.request import Request

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from app.models import Category
from app.serializers.category_serializer import CategorySerializer
from app.serializers.item_serializer import ItemSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True)
    def items(self, request: Request, *args, **kwargs) -> Response:
        # TODO: Pagination
        category_id: int = kwargs["pk"]

        instance: Category = self.queryset.model.objects.filter(id=category_id).first()
        if not instance:
            return Response("Invalid category id", status=status.HTTP_400_BAD_REQUEST)

        items: QuerySet = instance.items.filter(is_active=True)
        serializer: List[Dict[str, Any]] = ItemSerializer(items.order_by("-id"), many=True).data
        return Response(serializer)
