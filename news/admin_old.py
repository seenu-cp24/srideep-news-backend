from django.contrib import admin
from django.utils.html import format_html
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status_badge",
        "is_featured",
        "is_breaking",
        "published_at",
    )

    list_filter = (
        "status",
        "category",
        "is_featured",
        "is_breaking",
    )

    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)

    def status_badge(self, obj):
        colors = {
            "draft": "#6c757d",
            "published": "#198754",
            "archived": "#dc3545",
        }
        color = colors.get(obj.status, "#0d6efd")

        return format_html(
            '<span style="color:white; background:{}; padding:2px 6px; border-radius:4px;">{}</span>',
            color,
            obj.status.upper()
        )

    status_badge.short_description = "Status"
