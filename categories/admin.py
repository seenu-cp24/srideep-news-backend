from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "description_preview", "article_count", "created_at")
    search_fields = ("name", "slug")
    ordering = ("name",)

    prepopulated_fields = {"slug": ("name",)}

    readonly_fields = ("created_at",)

    def description_preview(self, obj):
        if obj.description:
            return obj.description[:40] + "..."
        return "-"
    description_preview.short_description = "Description"

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = "Articles"

