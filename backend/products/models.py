from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=50, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='styles')
    is_paid = models.BooleanField(default=False)
    prompt_template = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.genre.name}"


class StarPackage(models.Model):
    class Meta:
        verbose_name = 'Star Package'
        verbose_name_plural = 'Star Packages'
    
    name = models.CharField(max_length=32, unique=True)
    countries_t1 = models.CharField(max_length=255, blank=True, null=True)
    stars_count_t1 = models.IntegerField()
    stars_count_t2 = models.IntegerField()
    generations_count = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (T1 - {self.stars_count_t1}, T2 - {self.stars_count_t2})"