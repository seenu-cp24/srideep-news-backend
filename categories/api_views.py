"""
API Views for Categories
Clean, consistent, and ready for frontend integration.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import CategorySerializer


class CategoryListAPI(APIView):
    """
    Return all categories.
    Endpoint: /api/categories/
    """
    def get(self, request):
        qs = Category.objects.all().order_by("name")
        serializer = CategorySerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class CategoryDetailAPI(APIView):
    """
    Return a specific category by slug.
    Endpoint: /api/categories/<slug>/
    """
    def get(self, request, slug):
        obj = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(obj, context={"request": request})
        return Response(serializer.data)
