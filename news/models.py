from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from categories.models import Category
from authors.models import Author


class NewsArticle(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    # ---------------------------------------------------
    # Basic Content
    # ---------------------------------------------------
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)

    summary = models.TextField(blank=True, null=True)
    content = models.TextField()

    # ---------------------------------------------------
    # Metadata / SEO
    # ---------------------------------------------------
    seo_title = models.CharField(max_length=300, blank=True, null=True)
    seo_description = models.CharField(max_length=500, blank=True, null=True)

    # ---------------------------------------------------
    # Relations
    # ---------------------------------------------------
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )

    # ---------------------------------------------------
    # Media
    # ---------------------------------------------------
    featured_image = models.ImageField(
        upload_to="news/images/",
        blank=True,
        null=True
    )

    # ---------------------------------------------------
    # Flags
    # ---------------------------------------------------
    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)

    # ---------------------------------------------------
    # News Lifecycle Fields
    # ---------------------------------------------------
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------
    # Misc
    # ---------------------------------------------------
    reading_time = models.PositiveIntegerField(default=1)  # In minutes

    class Meta:
        ordering = ["-published_at", "-is_breaking", "-is_featured"]

    # ---------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------

    def generate_unique_slug(self):
        """
        Ensures slug uniqueness by appending incremental numbers.
        """
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while NewsArticle.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def calculate_reading_time(self):
        """
        Based on average reading speed of ~200 words/min.
        """
        word_count = len(self.content.split())
        return max(1, word_count // 200)

    def save(self, *args, **kwargs):
        # Auto slug generation
        if not self.slug:
            self.slug = self.generate_unique_slug()

        # Auto SEO title fallback
        if not self.seo_title:
            self.seo_title = self.title

        # Auto SEO description fallback
        if not self.seo_description and self.summary:
            self.seo_description = self.summary[:160]

        # Auto reading time
        self.reading_time = self.calculate_reading_time()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

