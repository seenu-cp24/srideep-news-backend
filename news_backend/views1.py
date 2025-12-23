from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.cache import never_cache

from news.models import NewsArticle


# =====================================================
# S3 TEST (KEEP AS IS)
# =====================================================
def test_s3(request):
    try:
        default_storage.save(
            "media_test.txt",
            ContentFile("S3 upload successful")
        )
        return HttpResponse("S3 upload OK")
    except Exception as e:
        return HttpResponse(f"S3 ERROR: {e}")


# =====================================================
# SOCIAL SHARE VIEW (CRITICAL FOR WHATSAPP / FB)
# =====================================================
@never_cache
def share_article(request, slug):
    """
    This view is ONLY for social media crawlers.
    It provides Open Graph meta tags (image, title, description)
    and then redirects the user to the frontend article page.
    """

    article = get_object_or_404(
        NewsArticle,
        slug=slug,
        status="published"
    )

    # 🔴 TEMP FRONTEND URL (CHANGE TO DOMAIN LATER)
    frontend_url = f"http://13.204.210.113:5173/article/{article.slug}"

    # Image priority:
    # 1. Featured image
    # 2. First gallery image
    og_image = ""
    if article.featured_image:
        og_image = article.featured_image.url
    elif article.gallery_images.exists():
        og_image = article.gallery_images.first().image.url

    og_title = article.seo_title or article.title
    og_description = article.seo_description or article.summary or article.title

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />

        <title>{og_title}</title>

        <!-- BASIC META -->
        <meta name="description" content="{og_description}" />

        <!-- OPEN GRAPH -->
        <meta property="og:type" content="article" />
        <meta property="og:title" content="{og_title}" />
        <meta property="og:description" content="{og_description}" />
        <meta property="og:image" content="{og_image}" />
        <meta property="og:url" content="{frontend_url}" />

        <!-- TWITTER -->
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="{og_title}" />
        <meta name="twitter:description" content="{og_description}" />
        <meta name="twitter:image" content="{og_image}" />

        <!-- REDIRECT USER -->
        <meta http-equiv="refresh" content="0; url={frontend_url}" />
    </head>

    <body>
        Redirecting to article…
    </body>
    </html>
    """

    return HttpResponse(html)
