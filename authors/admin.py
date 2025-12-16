from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "role",
        "created_at",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "name",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        ("User Info", {
            "fields": ("user", "name", "role"),
        }),
        ("Profile", {
            "fields": ("bio", "photo"),
        }),
        ("System", {
            "fields": ("created_at",),
        }),
    )
