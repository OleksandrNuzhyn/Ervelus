from django.contrib import admin
from .models import Style, SubscriptionPlan, Genre

admin.site.register(Style)
admin.site.register(SubscriptionPlan)
admin.site.register(Genre)