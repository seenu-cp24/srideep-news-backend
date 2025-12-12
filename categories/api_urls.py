from django.urls import path
from .views import CategoryListAPI

urlpatterns = [
    path("", CategoryListAPI.as_view(), name="category-list"),
]
