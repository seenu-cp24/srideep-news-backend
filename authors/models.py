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
        default="reporter",
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.name} ({self.role})"

    # -------------------------
    # Role helpers (CRITICAL)
    # -------------------------
    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_editor(self):
        return self.role == "editor"

    @property
    def is_reporter(self):
        return self.role == "reporter"

    # -------------------------
    # Optional auto-sync name
    # -------------------------
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.get_full_name() or self.user.username
        super().save(*args, **kwargs)
