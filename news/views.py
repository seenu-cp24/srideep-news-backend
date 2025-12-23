from django.shortcuts import get_object_or_404, render
from .models import NewsArticle

def article_share_view(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    return render(request, "news/article_share.html", {
        "article": article
    })
