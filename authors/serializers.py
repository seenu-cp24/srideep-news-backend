from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "bio",
            "photo_url",
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            try:
                return obj.photo.url
            except:
                return None
        return None
