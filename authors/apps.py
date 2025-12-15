from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authors"

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from .models import Author

        def create_author(sender, instance, created, **kwargs):
            if created:
                Author.objects.create(
                    user=instance,
                    name=instance.username,
                    role="admin" if instance.is_superuser else "reporter"
                )

        post_save.connect(create_author, sender=User)
