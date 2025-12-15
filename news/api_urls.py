"""
API URL routing for News module — clean and structured.
"""

from django.urls import path
from . import api_views

urlpatterns = [

    # ------------------------------------------------------------------
    # Main News List (Paginated)
    # ------------------------------------------------------------------
    path(
        "",
        api_views.NewsListAPI.as_view(),
        name="news-list"
    ),

    # ------------------------------------------------------------------
    # Latest News
    # ------------------------------------------------------------------
    path(
        "latest/",
        api_views.LatestNewsAPI.as_view(),
        name="news-latest"
    ),

    # ------------------------------------------------------------------
    # Featured News
    # ------------------------------------------------------------------
    path(
        "featured/",
        api_views.FeaturedNewsAPI.as_view(),
        name="news-featured"
    ),

    # ------------------------------------------------------------------
    # Category-wise Listing
    # ------------------------------------------------------------------
    path(
        "category/<slug:category_slug>/",
        api_views.NewsByCategoryAPI.as_view(),
        name="news-by-category"
    ),

    # ------------------------------------------------------------------
    # News Detail (SEO URL-Based)
    # Must be last to avoid conflicts
    # ------------------------------------------------------------------
    path(
        "<slug:slug>/",
        api_views.NewsDetailAPI.as_view(),
        name="news-detail"
    ),
]
