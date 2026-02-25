from payments.models import UserPurchase
from django.db.models import Sum, Count
from solo.models import SingletonModel
from users.models import UserProfile
from django.db import models


class Application(SingletonModel):
    is_free_generations_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Application"

    @property
    def users_count(self):
        users_count = UserProfile.objects.count()
        return f"{users_count}"

    @property
    def users_invites(self):
        data = UserProfile.objects.aggregate(users_invites=Sum('invited_count'))
        return data['users_invites'] or 0

    @property
    def users_organic_growth(self):
        data = UserProfile.objects.aggregate(users_invites=Sum('invited_count'), users_count=Count('id'))
        users_count = data['users_count'] or 0
        users_invites = data['users_invites'] or 0
        growth_rate = (users_invites / users_count) if users_count > 0 else 0
        return f"{growth_rate:.2f}"

    @property
    def users_geo_count(self):
        geo_data = UserProfile.objects.exclude(country_code__in=[None, '']).values('country_code').annotate(count=Count('id')).order_by('-count')
        geo_stats = [f"{c['country_code'].upper()}: {c['count']}" for c in geo_data]
        return "  |  ".join(geo_stats) if geo_stats else "No data"

    @property
    def paid_users_count(self):
        return UserProfile.objects.filter(is_paid=True).count()

    @property
    def sales_conversion_rate(self):
        users_count = UserProfile.objects.count()
        paid_users_count = UserProfile.objects.filter(is_paid=True).count()
        percent = (paid_users_count / users_count * 100) if users_count > 0 else 0
        return f"{percent:.1f}%"

    @property
    def sales_geo_count(self):
        geo_data = UserPurchase.objects.exclude(country_code__in=[None, '']).values('country_code').annotate(count=Count('id')).order_by('-count')
        geo_stats = [f"{c['country_code'].upper()}: {c['count']}" for c in geo_data]
        return "  |  ".join(geo_stats) if geo_stats else "No data"

    @property
    def sales_geo_stars(self):
        geo_data = UserPurchase.objects.exclude(country_code__in=[None, '']).values('country_code').annotate(stars_count=Sum('stars_count')).order_by('-stars_count')
        geo_stats = [f"{c['country_code'].upper()}: {c['stars_count']}" for c in geo_data]
        return "  |  ".join(geo_stats) if geo_stats else "No data"
    
    def __str__(self):
        return ""