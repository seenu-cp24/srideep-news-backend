from django.shortcuts import get_object_or_404, render
from news.models import NewsArticle

def news_share_view(request, slug):
    article = get_object_or_404(
        NewsArticle,
        slug=slug,
        status="published"
    )

    return render(
        request,
        "news/share.html",
        {
            "article": article,
            "share_url": f"https://www.srideepcomputers.com/article/{article.slug}",
        },
    )
