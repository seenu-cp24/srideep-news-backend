from django.contrib import admin
from django.utils.html import format_html
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "status_badge",
        "published_at",
    )
    list_filter = ("status", "category")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)

    def status_badge(self, obj):
        color_map = {
            "draft": "#6c757d",
            "review": "#0d6efd",
            "published": "#198754",
        }
        color = color_map.get(obj.status, "#000")
        return format_html(
            '<span style="color:white; background:{}; padding:2px 6px; border-radius:4px;">{}</span>',
            color,
            obj.status
        )

    status_badge.short_description = "Status"

    # ----------------------------
    # ROLE-BASED PERMISSIONS
    # ----------------------------
    def has_add_permission(self, request):
        return hasattr(request.user, "author_profile")

    def has_change_permission(self, request, obj=None):
        if not hasattr(request.user, "author_profile"):
            return False

        role = request.user.author_profile.role

        if role == "admin":
            return True
        if role == "editor":
            return True
        if role == "reporter":
            return False

        return False

    def has_delete_permission(self, request, obj=None):
        if not hasattr(request.user, "author_profile"):
            return False

        return request.user.author_profile.role == "admin"

    def save_model(self, request, obj, form, change):
        author = request.user.author_profile

        # Reporter → force draft
        if author.role == "reporter":
            obj.status = "draft"

        # Auto-assign author if missing
        if not obj.author_id:
            obj.author = author

        super().save_model(request, obj, form, change)
