"""
Serializers for News module — optimized for frontend UI, SEO, and API performance.
"""

from rest_framework import serializers
from .models import NewsArticle
from authors.serializers import AuthorSerializer
from categories.serializers import CategorySerializer


def pretty_date(dt):
    if not dt:
        return None
    return dt.strftime("%d %b %Y, %I:%M %p")


class NewsListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    read_time = serializers.IntegerField(source="reading_time", read_only=True)
    published_on = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "category",
            "author",
            "featured_image_url",
            "published_on",
            "read_time",
            "is_featured",
            "is_breaking",
        ]

    def get_featured_image_url(self, obj):
        try:
            if obj.featured_image:
                return obj.featured_image.url
        except:
            pass
        return None

    def get_published_on(self, obj):
        return pretty_date(obj.published_at)


class NewsDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    read_time = serializers.IntegerField(source="reading_time", read_only=True)
    published_on = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "category",
            "author",
            "featured_image_url",
            "published_on",
            "updated_on",
            "read_time",
            "seo_title",
            "seo_description",
            "is_featured",
            "is_breaking",
        ]

    def get_featured_image_url(self, obj):
        try:
            if obj.featured_image:
                return obj.featured_image.url
        except:
            pass
        return None

    def get_published_on(self, obj):
        return pretty_date(obj.published_at)

    def get_updated_on(self, obj):
        return pretty_date(obj.updated_at)
