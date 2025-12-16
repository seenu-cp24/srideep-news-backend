from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("editor", "Editor"),
        ("reporter", "Reporter"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="author_profile"
    )
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="authors/", blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reporter"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
