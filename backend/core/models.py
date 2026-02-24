from solo.models import SingletonModel
from users.models import UserProfile
from django.db.models import Sum
from django.db import models


class ApplicationAnalytics(SingletonModel):
    is_free_generations_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Application Analytics"

    @property
    def users_overview(self):
        total_users = UserProfile.objects.count()
        paid_users = UserProfile.objects.filter(is_paid=True).count()
        paid_users_percent = (paid_users / total_users * 100) if total_users > 0 else 0
        return f"Total: {total_users} | Paid: {paid_users} ({paid_users_percent:.1f}%)"

    @property
    def invites_overview(self):
        totals_data = UserProfile.objects.aggregate(
            total_invites=Sum('invited_count'),
            total_users=models.Count('id')
        )
        total_users = totals_data['total_users'] or 0
        total_invites = totals_data['total_invites'] or 0
        growth_rate = (total_invites / total_users) if total_users > 0 else 0
        return f"Total: {total_invites} | Organic Growth Rate: {growth_rate:.2f}"
    
    def __str__(self):
        return "Application Analytics"