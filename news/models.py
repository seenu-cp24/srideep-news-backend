from django.db import models
from django.utils.text import slugify
from categories.models import Category
from authors.models import Author


class NewsArticle(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    content = models.TextField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")

    featured_image = models.ImageField(upload_to="news/images/", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
