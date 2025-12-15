"""
API URL routing for Authors module — clean, structured, and scalable.
"""

from django.urls import path
from . import api_views

urlpatterns = [

    # --------------------------------------------------------------
    # List All Authors
    # --------------------------------------------------------------
    path(
        "",
        api_views.AuthorListAPI.as_view(),
        name="author-list"
    ),

    # --------------------------------------------------------------
    # Author Detail (by ID)
    # --------------------------------------------------------------
    path(
        "<int:pk>/",
        api_views.AuthorDetailAPI.as_view(),
        name="author-detail"
    ),

    # --------------------------------------------------------------
    # Author Detail (by slug)
    # More SEO-friendly, optional but useful for frontend
    # --------------------------------------------------------------
    path(
        "slug/<slug:slug>/",
        api_views.AuthorDetailBySlugAPI.as_view(),
        name="author-detail-slug"
    ),
]
