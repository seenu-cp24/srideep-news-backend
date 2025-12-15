"""
API URL routing for News module — stable & production-safe.
"""

from django.urls import path
from . import api_views

urlpatterns = [

    # -------------------------------------------------
    # News List (GET) + Create (POST)
    # -------------------------------------------------
    path(
        "",
        api_views.NewsListAPI.as_view(),
        name="news-list"
    ),

    # -------------------------------------------------
    # Latest News
    # -------------------------------------------------
    path(
        "latest/",
        api_views.LatestNewsAPI.as_view(),
        name="news-latest"
    ),

    # -------------------------------------------------
    # Featured News
    # -------------------------------------------------
    path(
        "featured/",
        api_views.FeaturedNewsAPI.as_view(),
        name="news-featured"
    ),

    # -------------------------------------------------
    # News by Category
    # -------------------------------------------------
    path(
        "category/<slug:category_slug>/",
        api_views.NewsByCategoryAPI.as_view(),
        name="news-by-category"
    ),

    # -------------------------------------------------
    # News Detail (GET / PUT / DELETE)
    # -------------------------------------------------
    path(
        "<slug:slug>/",
        api_views.NewsDetailAPI.as_view(),
        name="news-detail"
    ),
]
