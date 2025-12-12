from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import NewsArticle
from .serializers import NewsListSerializer, NewsDetailSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class NewsListAPI(APIView):
    def get(self, request):
        qs = NewsArticle.objects.filter(status="published").order_by("-published_at")
        # optional search
        q = request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(summary__icontains=q)
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = NewsListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

class NewsDetailAPI(APIView):
    def get(self, request, slug):
        obj = get_object_or_404(NewsArticle, slug=slug, status="published")
        serializer = NewsDetailSerializer(obj, context={"request": request})
        return Response(serializer.data)

class NewsByCategoryAPI(APIView):
    def get(self, request, category_slug):
        qs = NewsArticle.objects.filter(status="published", category__slug=category_slug).order_by("-published_at")
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = NewsListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

class LatestNewsAPI(APIView):
    def get(self, request):
        limit = int(request.GET.get("limit", 5))
        qs = NewsArticle.objects.filter(status="published").order_by("-published_at")[:limit]
        serializer = NewsListSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

class FeaturedNewsAPI(APIView):
    def get(self, request):
        qs = NewsArticle.objects.filter(status="published", featured_image__isnull=False).order_by("-published_at")[:10]
        serializer = NewsListSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)
