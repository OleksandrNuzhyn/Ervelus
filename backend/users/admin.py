from django.contrib import admin
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialApp, SocialToken
from . import services
from .forms import EmailForm
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from rest_framework.authtoken.models import TokenProxy
from core.admin_mixins import NoLogAdminMixin
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from allauth.account.admin import EmailAddressAdmin
from allauth.socialaccount.admin import SocialAccountAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(TOTPDevice)
admin.site.unregister(TokenProxy)

EmailAddress._meta.verbose_name = "Email Address"
EmailAddress._meta.verbose_name_plural = "Email Addresses"
SocialAccount._meta.verbose_name = "Social Account"
SocialAccount._meta.verbose_name_plural = "Social Accounts"
TOTPDevice._meta.verbose_name = "TOTP Device"
TOTPDevice._meta.verbose_name_plural = "TOTP Devices"


@admin.register(User)
class UserAdmin(NoLogAdminMixin, BaseUserAdmin):
    change_list_template = "admin/users/user/change_list.html"
    change_form_template = "admin/users/user/change_form.html"
    list_display = ('id', 'email', 'username', 'is_active', 'date_joined_formatted', 'last_login_formatted')
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-mailgun-list/', self.admin_site.admin_view(self.sync_mailgun_list_view), name='sync-mailgun-list-view'),
            path('send-group-email/', self.admin_site.admin_view(self.send_group_email_view), name='send-group-email-view'),
            path('<path:user_id>/send-email/', self.admin_site.admin_view(self.send_email_view), name='send-email-view')
        ]

        return custom_urls + urls

    def sync_mailgun_list_view(self, request):
        result = services.sync_users_with_mailgun_list()

        if result["is_success"]:
            self.message_user(request, result["message"], messages.SUCCESS)
        else:
            self.message_user(request, result["message"], messages.ERROR)
        
        return HttpResponseRedirect("../")

    def send_group_email_view(self, request):
        form = EmailForm(request.POST or None)
        
        if request.method == 'POST' and form.is_valid():
            template_name = form.cleaned_data['template']
            result = services.send_email(settings.MAILGUN_MAILING_LIST_ADDRESS, template_name)

            if result["is_success"]:
                self.message_user(request, result["message"], messages.SUCCESS)
            else:
                self.message_user(request, result["message"], messages.ERROR)

            return HttpResponseRedirect("../")

        context = self.admin_site.each_context(request)
        context['form'] = form
        context['title'] = "Send Group Email"
        context['submit_button_text'] = "Send Emails to all users"
        
        return render(request, 'admin/users/user/send_email.html', context)

    def send_email_view(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = EmailForm(request.POST or None)
        
        if request.method == 'POST' and form.is_valid():
            template_name = form.cleaned_data['template']
            
            result = services.send_email(user.email, template_name)

            if result["is_success"]:
                self.message_user(request, result["message"], messages.SUCCESS)
            else:
                self.message_user(request, result["message"], messages.ERROR)

            return HttpResponseRedirect("../")

        context = self.admin_site.each_context(request)
        context['form'] = form
        context['title'] = f"Send Email to {user.email}"
        context['submit_button_text'] = f"Send Email to {user.email}"
        
        return render(request, 'admin/users/user/send_email.html', context)


@admin.register(UserProfile)
class UserProfileAdmin(NoLogAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user__email', 'telegram_id', 'credits')
    list_select_related = ('user',)
    search_fields = ('user__email', 'telegram_id')
    readonly_fields = ('user',)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EmailAddress)
class CustomEmailAddressAdmin(NoLogAdminMixin, EmailAddressAdmin):
    list_display = ('id', 'email', 'verified')
    list_filter = ('verified',)
    search_fields = ('email',)
    readonly_fields = ('user', 'email', 'primary')
    ordering = ('-id',)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialAccount)
class CustomSocialAccountAdmin(NoLogAdminMixin, SocialAccountAdmin):
    list_display = ('id', 'user__email', 'date_joined_formatted', 'last_login_formatted')
    list_select_related = ('user',)
    list_filter = ('date_joined', 'last_login')
    search_fields = ('user__email', 'extra_data')
    readonly_fields = ('user', 'uid', 'provider', 'date_joined_formatted', 'last_login_formatted', 'extra_data')
    ordering = ('-id',)

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


@admin.register(TOTPDevice)
class CustomTOTPDeviceAdmin(TOTPDeviceAdmin):
    list_display = ('id', 'user__email', 'name', 'confirmed', 'created_at_formatted', 'last_used_at_formatted')
    list_select_related = ('user',)
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