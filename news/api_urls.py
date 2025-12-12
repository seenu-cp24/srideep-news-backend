from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.NewsListAPI.as_view(), name="news-list"),
    path("latest/", api_views.LatestNewsAPI.as_view(), name="news-latest"),
    path("featured/", api_views.FeaturedNewsAPI.as_view(), name="news-featured"),
    path("category/<slug:category_slug>/", api_views.NewsByCategoryAPI.as_view(), name="news-by-category"),
    path("<slug:slug>/", api_views.NewsDetailAPI.as_view(), name="news-detail"),
]
