"""
Author API Views — clean, optimized, paginated, and SEO-friendly.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Author
from .serializers import AuthorSerializer


# -----------------------------------------------------------
# Pagination class (same standard for all modules)
# -----------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -----------------------------------------------------------
# List Authors (paginated + optional search)
# -----------------------------------------------------------
class AuthorListAPI(APIView):
    def get(self, request):
        qs = Author.objects.all().order_by("name")

        # Optional search by name
        q = request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = AuthorSerializer(page, many=True, context={"request": request})

        return paginator.get_paginated_response(serializer.data)


# -----------------------------------------------------------
# Author Detail (by ID)
# -----------------------------------------------------------
class AuthorDetailAPI(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(obj, context={"request": request})
        return Response(serializer.data)


# -----------------------------------------------------------
# Author Detail (SEO-friendly slug)
# -----------------------------------------------------------
class AuthorDetailBySlugAPI(APIView):
    def get(self, request, slug):
        obj = get_object_or_404(Author, slug=slug)
        serializer = AuthorSerializer(obj, context={"request": request})
        return Response(serializer.data)
