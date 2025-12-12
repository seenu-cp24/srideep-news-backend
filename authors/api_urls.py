from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.AuthorListAPI.as_view(), name="author-list"),
    path("<int:pk>/", api_views.AuthorDetailAPI.as_view(), name="author-detail"),
]
