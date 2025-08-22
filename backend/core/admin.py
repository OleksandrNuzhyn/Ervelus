from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import ApplicationConfig


admin.site.register(ApplicationConfig, SingletonModelAdmin)