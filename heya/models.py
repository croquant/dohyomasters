from django.db import models

from base.models import AlphaIDField, User


class Heya(models.Model):
    id = AlphaIDField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    name_jp = models.CharField(max_length=32, unique=True)
    master = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="heya"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Heya"
