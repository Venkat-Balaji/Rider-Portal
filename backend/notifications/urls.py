# notifications/urls.py
from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('<uuid:id>/mark-read', MarkNotificationReadView.as_view(), name='notification-mark-read'),
]
