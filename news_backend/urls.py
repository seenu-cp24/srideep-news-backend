from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

# -----------------------------------
# Swagger / Redoc Documentation
# -----------------------------------
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Srideep News API",
        default_version='v1',
        description="API Documentation for Srideep News Platform",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# -----------------------------------
# ENV TEST
# -----------------------------------
def test_env(request):
    return JsonResponse({
        "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "AWS_STORAGE_BUCKET_NAME": os.environ.get("AWS_STORAGE_BUCKET_NAME"),
        "AWS_S3_REGION_NAME": os.environ.get("AWS_S3_REGION_NAME"),
        "AWS_S3_SIGNATURE_VERSION": os.environ.get("AWS_S3_SIGNATURE_VERSION"),
    })


# -----------------------------------
# S3 UPLOAD TEST
# -----------------------------------
def test_s3_upload(request):
    filename = "media/test_upload_final.txt"
    default_storage.save(filename, ContentFile("S3 WORKING"))
    return JsonResponse({"status": "ok", "file": filename})


# -----------------------------------
# URL ROUTING
# -----------------------------------
urlpatterns = [

    # IMPORTANT — swagger must be at the top
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc"),

    path("admin/", admin.site.urls),

    # Test URLs
    path("test-env/", test_env),
    path("test-s3-upload/", test_s3_upload),

    # API Routes
    path("api/categories/", include("categories.api_urls")),
    path("api/news/", include("news.api_urls")),
    path("api/authors/", include("authors.api_urls")),
]
