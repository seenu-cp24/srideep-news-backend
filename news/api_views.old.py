"""
API Views for the News module
Clean, optimized, frontend-ready, and JWT-compatible
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import NewsArticle
from .serializers import NewsListSerializer, NewsDetailSerializer


# ----------------------------------------------------------------------
# Pagination
# ----------------------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


# ----------------------------------------------------------------------
# News List API (Public)
# ----------------------------------------------------------------------
class NewsListAPI(APIView):
    """
    Returns paginated list of all published news.
    Optional search using ?q=keyword
    """
    permission_classes = [AllowAny]

    def get(self, request):
        qs = (
            NewsArticle.objects.filter(status="published")
            .select_related("category", "author")
            .order_by("-published_at")
        )

        # Optional search
        q = request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(summary__icontains=q)
                | Q(content__icontains=q)
            )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)

        serializer = NewsListSerializer(
            page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


# ----------------------------------------------------------------------
# News Detail API (Public)
# ----------------------------------------------------------------------
class NewsDetailAPI(APIView):
    """
    Returns full details of a news article
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        article = get_object_or_404(
            NewsArticle.objects.select_related("category", "author"),
            slug=slug,
            status="published",
        )

        serializer = NewsDetailSerializer(
            article, context={"request": request}
        )
        return Response(serializer.data)


# ----------------------------------------------------------------------
# News by Category API (Public)
# ----------------------------------------------------------------------
class NewsByCategoryAPI(APIView):
    """
    Returns paginated news list for a specific category.
    """
    permission_classes = [AllowAny]

    def get(self, request, category_slug):
        qs = (
            NewsArticle.objects.filter(
                status="published",
                category__slug=category_slug
            )
            .select_related("category", "author")
            .order_by("-published_at")
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)

        serializer = NewsListSerializer(
            page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


# ----------------------------------------------------------------------
# Latest News API (Public)
# ----------------------------------------------------------------------
class LatestNewsAPI(APIView):
    """
    Returns the latest N news items.
    Usage: /api/news/latest/?limit=10
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            limit = int(request.GET.get("limit", 5))
            limit = max(1, min(limit, 50))
        except ValueError:
            limit = 5

        qs = (
            NewsArticle.objects.filter(status="published")
            .select_related("category", "author")
            .order_by("-published_at")[:limit]
        )

        serializer = NewsListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)


# ----------------------------------------------------------------------
# Featured News API (Public)
# ----------------------------------------------------------------------
class FeaturedNewsAPI(APIView):
    """
    Returns featured news (with image).
    Limit = 10 articles.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        qs = (
            NewsArticle.objects.filter(
                status="published",
                is_featured=True
            )
            .select_related("category", "author")
            .order_by("-published_at")[:10]
        )

        serializer = NewsListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)
