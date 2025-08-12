from django.contrib import admin
from .models import UserProfile


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