from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import ApplicationConfig


@admin.register(ApplicationConfig)
class ApplicationConfigAdmin(SingletonModelAdmin):
    readonly_fields = ('reserved_for_spend',)