from django.urls import path
from . import webhooks


urlpatterns = [
    path('tasks/', webhooks.tasks_handler, name='tasks-handler')
]