"""
News API — Stable, JWT-secured, role-aware
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
from .permissions import IsAdminEditorReporter


# -------------------------------------------------
# Pagination
# -------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# =================================================
# PUBLIC APIs
# =================================================

class NewsListAPI(APIView):
    """Public news list"""
    permission_classes = []

    def get(self, request):
        qs = (
            NewsArticle.objects
            .filter(status="published")
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


class NewsDetailAPI(APIView):
    """Public news detail"""
    permission_classes = []

    def get(self, request, slug):
        article = get_object_or_404(
            NewsArticle,
            slug=slug,
            status="published"
        )
        serializer = NewsDetailSerializer(article, context={"request": request})
        return Response(serializer.data)


class NewsByCategoryAPI(APIView):
    permission_classes = []

    def get(self, request, category_slug):
        qs = (
            NewsArticle.objects
            .filter(status="published", category__slug=category_slug)
            .select_related("category", "author")
            .order_by("-published_at")
        )

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = NewsListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class LatestNewsAPI(APIView):
    permission_classes = []

    def get(self, request):
        try:
            limit = min(int(request.GET.get("limit", 5)), 50)
        except ValueError:
            limit = 5

        qs = (
            NewsArticle.objects
            .filter(status="published")
            .order_by("-published_at")[:limit]
        )

        serializer = NewsListSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class FeaturedNewsAPI(APIView):
    permission_classes = []

    def get(self, request):
        qs = (
            NewsArticle.objects
            .filter(status="published", is_featured=True)
            .order_by("-published_at")[:10]
        )

        serializer = NewsListSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


# =================================================
# MANAGEMENT APIs (JWT REQUIRED)
# =================================================

class NewsCreateAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminEditorReporter]

    def post(self, request):
        if not hasattr(request.user, "author_profile"):
            return Response(
                {"detail": "Author profile not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        author = request.user.author_profile
        data = request.data.copy()

        # Reporter → draft only
        if author.role == "reporter":
            data["status"] = "draft"

        serializer = NewsDetailSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsUpdateDeleteAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminEditorReporter]

    def put(self, request, slug):
        article = get_object_or_404(NewsArticle, slug=slug)
        author = request.user.author_profile

        if author.role == "reporter":
            return Response(
                {"detail": "Reporters cannot update articles"},
                status=status.HTTP_403_FORBIDDEN
            )

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
        author = request.user.author_profile

        if author.role != "admin":
            return Response(
                {"detail": "Only admins can delete articles"},
                status=status.HTTP_403_FORBIDDEN
            )

        article = get_object_or_404(NewsArticle, slug=slug)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------
# MY ARTICLES (JWT REQUIRED)
# -------------------------------------------------
class MyArticlesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "author_profile"):
            return Response(
                {"detail": "Author profile not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        author = request.user.author_profile

        qs = (
            NewsArticle.objects
            .filter(author=author)
            .select_related("category", "author")
            .order_by("-id")   # ✅ FIXED (was created_at)
        )

        serializer = NewsListSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)

# -------------------------------------------------
# SUBMIT FOR REVIEW (REPORTER)
# -------------------------------------------------
class SubmitForReviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        author = request.user.author_profile
        article = get_object_or_404(
            NewsArticle,
            slug=slug,
            author=author
        )

        if article.status != "draft":
            return Response(
                {"detail": "Only draft articles can be submitted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        article.status = "review"
        article.save()

        return Response(
            {"detail": "Article submitted for review"},
            status=status.HTTP_200_OK
        )


# -------------------------------------------------
# PUBLISH ARTICLE (EDITOR / ADMIN)
# -------------------------------------------------
class PublishArticleAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminEditorReporter]

    def post(self, request, slug):
        author = request.user.author_profile

        if author.role not in ["admin", "editor"]:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        article = get_object_or_404(NewsArticle, slug=slug)

        if article.status != "review":
            return Response(
                {"detail": "Only reviewed articles can be published"},
                status=status.HTTP_400_BAD_REQUEST
            )

        article.status = "published"
        article.save()

        return Response(
            {"detail": "Article published successfully"},
            status=status.HTTP_200_OK
        )
