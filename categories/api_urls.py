"""
Category API URL routing — clean, structured, SEO-friendly.
"""

from django.urls import path
from . import api_views

urlpatterns = [
    # List all categories
    path("", api_views.CategoryListAPI.as_view(), name="category-list"),

    # Category detail by slug
    path("<slug:slug>/", api_views.CategoryDetailAPI.as_view(), name="category-detail"),
]
