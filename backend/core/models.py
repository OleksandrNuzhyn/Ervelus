from solo.models import SingletonModel
from django.db import models


class ApplicationConfig(SingletonModel):
    generations_reserved = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Application Configuration"

    def __str__(self):
        return "Application Configuration"