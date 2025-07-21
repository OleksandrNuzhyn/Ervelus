from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=50, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='styles')
    prompt_template = models.TextField()
    preview_image_url = models.URLField()

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

    name = models.CharField(max_length=25, unique=True)
    unlocked_styles = models.ManyToManyField(Style)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    paddle_plan_id = models.CharField(max_length=6, unique=True)
    generations_count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    total_price_usage = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name