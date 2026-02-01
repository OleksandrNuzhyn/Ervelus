from core.admin_mixins import NoLogAdminMixin
from django.utils import timezone
from django.contrib import admin
from .models import UserPurchase


@admin.register(UserPurchase)
class UserPurchaseAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ("id", "stars_count", "generations_count", "country_code", "purchased_at_formatted")
    list_select_related = ("user",)
    list_filter = ("purchased_at",)
    search_fields = ("user__email", "transaction_id", "country_code")
    ordering = ("-purchased_at",)
    raw_id_fields = ("user",)

    @admin.display(ordering='purchased_at', description='purchased at')
    def purchased_at_formatted(self, obj):
        return timezone.localtime(obj.purchased_at).strftime('%d.%m.%Y %H:%M:%S')