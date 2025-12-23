from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import NewsArticle


def share_article(request, slug):
    article = get_object_or_404(
        NewsArticle,
        slug=slug,
        status="published"
    )

    # IMPORTANT: frontend dev URL (IP based)
    frontend_url = f"http://13.204.210.113:5173/article/{article.slug}"

    context = {
        "title": article.seo_title or article.title,
        "description": article.seo_description or article.summary,
        "image": article.featured_image.url if article.featured_image else "",
        "url": frontend_url,
    }

    html = render_to_string("share_article.html", context)
    return HttpResponse(html)
