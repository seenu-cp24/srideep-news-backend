"""
URL configuration for news_backend project.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import path, include
import os


# ---------------------------
# ENV TEST ENDPOINT
# ---------------------------
def test_env(request):
    return JsonResponse({
        "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "AWS_STORAGE_BUCKET_NAME": os.environ.get("AWS_STORAGE_BUCKET_NAME"),
        "AWS_S3_REGION_NAME": os.environ.get("AWS_S3_REGION_NAME"),
        "AWS_S3_SIGNATURE_VERSION": os.environ.get("AWS_S3_SIGNATURE_VERSION"),
    })


# ---------------------------
# S3 UPLOAD TEST ENDPOINT
# ---------------------------
def test_s3_upload(request):
    filename = "media/test_upload_final.txt"
    default_storage.save(filename, ContentFile("S3 WORKING"))
    return JsonResponse({"status": "ok", "file": filename})


# ---------------------------
# URL ROUTING
# ---------------------------
urlpatterns = [
    path('admin/', admin.site.urls),

    # Environment variable test
    path('test-env/', test_env),

    # S3 upload test
    path('test-s3-upload/', test_s3_upload),

    # API Routes
    # API routes
    path('api/categories/', include('categories.api_urls')),
    path('api/news/', include('news.api_urls')),
    path('api/authors/', include('authors.api_urls')),  # we'll create authors.api_urls below
]

