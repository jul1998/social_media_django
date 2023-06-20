from django.urls import path, include
from . import views

urlpatterns = [
    path('notify/', views.notify_when_liked, name='notify'), 
    path('get-notifications/<int:user_id>/', views.get_notifications, name='get_notifications'), 
    path('show-active-notifications/<int:user_id>/', views.show_not_seen_notifications, name='show_active_notifications'),
    path('set-notification-seen/', views.set_notification_seen, name='set_notification_seen')

]
