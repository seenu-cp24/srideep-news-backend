from rest_framework import serializers
from .models import NewsArticle
from authors.serializers import AuthorSerializer
from categories.serializers import CategorySerializer

class NewsListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id", "title", "slug", "summary", "category", "author",
            "featured_image_url", "status", "published_at",
        ]

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            try:
                return obj.featured_image.url
            except Exception:
                return None
        return None


class NewsDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id", "title", "slug", "summary", "content", "category",
            "author", "featured_image_url", "status", "published_at", "updated_at",
        ]

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            try:
                return obj.featured_image.url
            except Exception:
                return None
        return None
