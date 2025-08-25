from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import services
from django.shortcuts import render, get_object_or_404
from .forms import EmailForm
from django.conf import settings

User = get_user_model()
admin.site.unregister(User)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_credits')
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
    change_form_template = "admin/users/user/change_form.html"

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