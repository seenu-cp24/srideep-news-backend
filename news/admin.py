from django.contrib import admin
from .models import NewsArticle

@admin.register(NewsArticle)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "status", "published_at")
    list_filter = ("status", "category")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
