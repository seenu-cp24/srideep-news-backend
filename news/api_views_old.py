"""
API Views for the News module — secure, stable, and production-ready.
(Current version WITHOUT role-based logic)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import NewsArticle
from .serializers import NewsListSerializer, NewsDetailSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly


# -------------------------------------------------
# Pagination
# -------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -------------------------------------------------
# NEWS LIST (PUBLIC)
# -------------------------------------------------
class NewsListAPI(APIView):
    """
    GET  → Public
    POST → Admin / Editor / Reporter (JWT required)
    """
    permission_classes = [IsAuthenticated | IsAdminEditorReporter]

    def get(self, request):
        qs = (
            NewsArticle.objects.filter(status="published")
            .select_related("category", "author")
            .order_by("-published_at")
        )

        q = request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(summary__icontains=q)
                | Q(content__icontains=q)
            )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = NewsListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        author = request.user.author_profile
        data = request.data.copy()

        # Reporter → draft only
        if author.role == "reporter":
            data["status"] = "draft"

        serializer = NewsDetailSerializer(
            data=data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# -------------------------------------------------
# NEWS DETAIL (PUBLIC READ)
# -------------------------------------------------
class NewsDetailAPI(APIView):
    permission_classes = []

    def get(self, request, slug):
        article = get_object_or_404(
            NewsArticle.objects.select_related("category", "author"),
            slug=slug,
            status="published"
        )
        serializer = NewsDetailSerializer(article, context={"request": request})
        return Response(serializer.data)


# -------------------------------------------------
# NEWS UPDATE / DELETE (ADMIN ONLY)
# -------------------------------------------------
class NewsUpdateDeleteAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, slug):
        article = get_object_or_404(NewsArticle, slug=slug)
        serializer = NewsDetailSerializer(
            article,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        article = get_object_or_404(NewsArticle, slug=slug)
        article.delete()
        return Response(
            {"detail": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# -------------------------------------------------
# NEWS BY CATEGORY (PUBLIC)
# -------------------------------------------------
class NewsByCategoryAPI(APIView):
    permission_classes = []

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


# -------------------------------------------------
# LATEST NEWS (PUBLIC)
# -------------------------------------------------
class LatestNewsAPI(APIView):
    permission_classes = []

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


# -------------------------------------------------
# FEATURED NEWS (PUBLIC)
# -------------------------------------------------
class FeaturedNewsAPI(APIView):
    permission_classes = []

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
