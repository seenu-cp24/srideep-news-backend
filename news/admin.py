from django.contrib import admin
from django.utils.html import format_html
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsAdmin(admin.ModelAdmin):

    # Columns visible in list page
    list_display = (
        "thumbnail",
        "title",
        "category",
        "author",
        "status_badge",
        "is_featured",
        "is_breaking",
        "published_at",
    )

    list_filter = ("status", "category", "is_featured", "is_breaking")
    search_fields = ("title", "summary", "content")
    ordering = ("-published_at", "-updated_at")

    # Auto slug
    prepopulated_fields = {"slug": ("title",)}

    # Read-only timestamps
    readonly_fields = ("published_at", "updated_at")

    # Admin form layout
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "summary", "content", "category", "author")
        }),
        ("Media", {
            "fields": ("featured_image",)
        }),
        ("SEO Fields", {
            "fields": ("seo_title", "seo_description"),
            "classes": ("collapse",)
        }),
        ("Status & Flags", {
            "fields": ("status", "is_featured", "is_breaking")
        }),
        ("Timestamps", {
            "fields": ("published_at", "updated_at")
        }),
    )

    # --------------------- Custom Display Methods ------------------------

    def thumbnail(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit:cover;" />',
                obj.featured_image.url,
            )
        return "No Image"

    thumbnail.short_description = "Image"

    def status_badge(self, obj):
        color = "green" if obj.status == "published" else "orange"
        return format_html(f'<span style="color:white; background:{color}; padding:2px 6px; border-radius:4px;">{obj.status}</span>')

    status_badge.short_description = "Status"
