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
    # My Articles (JWT)
    # -------------------------------------------------
    path(
        "manage/my-articles/",
        api_views.MyArticlesAPI.as_view(),
        name="news-my-articles"
    ),
    path("manage/create/", api_views.NewsCreateAPI.as_view()),
    path("manage/<slug:slug>/", api_views.NewsUpdateDeleteAPI.as_view()),


    # -------------------------------------------------
    # Workflow APIs
    # -------------------------------------------------
    path(
        "manage/submit/<slug:slug>/",
        api_views.SubmitForReviewAPI.as_view(),
        name="news-submit-review"
    ),

    path(
        "manage/publish/<slug:slug>/",
        api_views.PublishArticleAPI.as_view(),
        name="news-publish"
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
