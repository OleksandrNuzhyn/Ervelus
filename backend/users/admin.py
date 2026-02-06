from django.contrib import admin
from .models import UserProfile
from django.utils import timezone
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from rest_framework.authtoken.models import TokenProxy
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.admin_mixins import NoLogAdminMixin

User = get_user_model()

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(TOTPDevice)
admin.site.unregister(TokenProxy)

TOTPDevice._meta.verbose_name = "TOTP Device"
TOTPDevice._meta.verbose_name_plural = "TOTP Devices"


@admin.register(User)
class UserAdmin(NoLogAdminMixin, BaseUserAdmin):
    list_display = ('id', 'username', 'date_joined_formatted', 'last_login_formatted', 'is_active')
    list_filter = ('is_active', 'date_joined', 'last_login', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-id',)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (("Important dates"), {"fields": ("last_login", "date_joined")})
    )

    @admin.display(ordering='last_login', description='last login')
    def last_login_formatted(self, obj):
        if obj.last_login:
            return timezone.localtime(obj.last_login).strftime('%d.%m.%Y %H:%M:%S')
        return None

    @admin.display(ordering='date_joined', description='date joined')
    def date_joined_formatted(self, obj):
        return timezone.localtime(obj.date_joined).strftime('%d.%m.%Y %H:%M:%S')

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UserProfile)
class UserProfileAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'country_code', 'credits')
    search_fields = ('user__email', 'telegram_id', 'country_code')
    readonly_fields = ('user',)
    ordering = ('-credits',)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TOTPDevice)
class CustomTOTPDeviceAdmin(TOTPDeviceAdmin):
    list_display = ('id', 'name', 'last_used_at_formatted', 'confirmed')
    search_fields = ('user__email', 'name')
    readonly_fields = ('created_at_formatted', 'last_used_at_formatted', 'qrcode_link')
    ordering = ('-id',)

    @admin.display(ordering='created_at', description='created at')
    def created_at_formatted(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d.%m.%Y %H:%M:%S')
    
    @admin.display(ordering='last_used_at', description='last used at')
    def last_used_at_formatted(self, obj):
        if obj.last_used_at:
            return timezone.localtime(obj.last_used_at).strftime('%d.%m.%Y %H:%M:%S')
        return None

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Identity', {'fields': ['user', 'name', 'confirmed']}),
            ('Timestamps', {'fields': ['created_at_formatted', 'last_used_at_formatted']}),
            ('QR Code', {'fields': ['qrcode_link']})
        ]

        return fieldsets