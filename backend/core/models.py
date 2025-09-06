from django.db import models
from solo.models import SingletonModel


class ApplicationConfig(SingletonModel):
    is_registration_enabled = models.BooleanField(default=True)
    hard_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reserved_for_spend = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Application Configuration"

    def __str__(self):
        return "Application Configuration"