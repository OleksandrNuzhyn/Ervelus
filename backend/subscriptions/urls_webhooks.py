from django.urls import path
from . import webhooks


urlpatterns = [
    path('wayforpay/', webhooks.wayforpay_handler, name='wayforpay-handler'),
    path('tasks/', webhooks.tasks_handler, name='tasks-handler')
]