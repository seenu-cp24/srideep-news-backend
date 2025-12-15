"""
API Views for the News module — optimized, clean, and production-ready.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import NewsArticle
from .serializers import NewsListSerializer, NewsDetailSerializer


# ----------------------------------------------------------------------
# Pagination Settings
# ----------------------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ----------------------------------------------------------------------
# News List API
# ----------------------------------------------------------------------
class NewsListAPI(APIView):
    """
    Returns paginated list of all published news.
    Optional search using ?q=keyword
    """
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
# News Detail API (with Related Articles)
# ----------------------------------------------------------------------
class NewsDetailAPI(APIView):
    """
    Returns full details of a news article and 5 related articles.
    """
    def get(self, request, slug):
        # Current article
        obj = get_object_or_404(
            NewsArticle.objects.select_related("category", "author"),
            slug=slug, status="published"
        )

        data = NewsDetailSerializer(obj, context={"request": request}).data

        # Related Articles — Same category
        related = (
            NewsArticle.objects.filter(
                status="published",
                category=obj.category
            )
            .exclude(id=obj.id)
            .order_by("-published_at")[:5]
        )

        related_serialized = NewsListSerializer(
            related, many=True, context={"request": request}
        ).data

        return Response({
            "article": data,
            "related_articles": related_serialized
        })


# ----------------------------------------------------------------------
# News by Category API
# ----------------------------------------------------------------------
class NewsByCategoryAPI(APIView):
    """
    Returns paginated news list for a specific category.
    """
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
# Latest News API
# ----------------------------------------------------------------------
class LatestNewsAPI(APIView):
    """
    Returns the latest N news items.
    Usage: /api/news/latest/?limit=10
    """
    def get(self, request):
        try:
            limit = int(request.GET.get("limit", 5))
            limit = max(1, min(limit, 50))  # clamp between 1 and 50
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
# Featured News API
# ----------------------------------------------------------------------
class FeaturedNewsAPI(APIView):
    """
    Returns news that have featured images.
    Limit = 10 articles.
    """
    def get(self, request):
        qs = (
            NewsArticle.objects.filter(
                status="published",
                featured_image__isnull=False
            )
            .select_related("category", "author")
            .order_by("-published_at")[:10]
        )

        serializer = NewsListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)
