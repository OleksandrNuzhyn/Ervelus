from solo.models import SingletonModel
from users.models import UserProfile
from django.db.models import Sum
from django.db import models


class ApplicationConfig(SingletonModel):
    reserved_generations = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Application Configuration"
    
    @property
    def unused_generations(self):
        return UserProfile.objects.aggregate(total_generations=Sum('credits'))['total_generations'] or 0

    def __str__(self):
        return "Application Configuration"