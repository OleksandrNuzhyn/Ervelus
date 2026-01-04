from django.contrib import admin
from django.utils import timezone
from core.admin_mixins import NoLogAdminMixin
from .models import PromoCode, PromoCodeUsage


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'max_usages', 'current_usages', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'description')
    ordering = ('-id',)


@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('user__email', 'promo_code', 'used_at_formatted')
    list_select_related = ('user', 'promo_code')
    list_filter = ('promo_code',)
    search_fields = ('user__email',)
    ordering = ('-used_at',)
    raw_id_fields = ('user', 'promo_code')

    @admin.display(ordering='used_at', description='used at')
    def used_at_formatted(self, obj):
        return timezone.localtime(obj.used_at).strftime('%d.%m.%Y %H:%M:%S')