from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(source="articles.count", read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "article_count",
        ]
