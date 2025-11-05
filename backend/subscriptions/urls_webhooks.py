from django.urls import path
from . import webhooks


urlpatterns = [
    path('paddle/', webhooks.paddle_handler, name='paddle-handler'),
    path('tasks/', webhooks.tasks_handler, name='tasks-handler')
]