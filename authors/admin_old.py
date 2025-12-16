from django.contrib import admin
from django.utils.html import format_html
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ("photo_thumb", "name", "bio_preview", "created_at")
    search_fields = ("name",)
    ordering = ("name",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "bio")
        }),
        ("Photo", {
            "fields": ("photo",)
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )

    # Thumbnail in admin list
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:4px;" />',
                obj.photo.url,
            )
        return "No Image"
    photo_thumb.short_description = "Photo"

    def bio_preview(self, obj):
        return (obj.bio[:50] + "...") if obj.bio else "-"
    bio_preview.short_description = "Bio"
