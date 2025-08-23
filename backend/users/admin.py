from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import services

User = get_user_model()
admin.site.unregister(User)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'accepted_terms_version', 'total_credits')
    list_select_related = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate_total_credits()

    @admin.display(ordering='total_credits', description='total credits')
    def total_credits(self, obj):
        return obj.total_credits


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    change_list_template = "admin/users/user/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-mailgun-list/', self.admin_site.admin_view(self.sync_mailgun_list_view), name='sync_mailgun_list_view')
        ]

        return custom_urls + urls

    def sync_mailgun_list_view(self, request):
        result = services.sync_users_with_mailgun_list()

        if result["is_success"]:
            self.message_user(request, result["message"], messages.SUCCESS)
        else:
            self.message_user(request, result["message"], messages.ERROR)
        
        return HttpResponseRedirect("../")