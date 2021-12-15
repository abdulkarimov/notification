from django.urls import path, include
from notification.views import NotificationView
app_name = 'notifications'
urlpatterns = [
    path('notifications/', NotificationView.as_view()),
    path('notifications/<int:pk>', NotificationView.as_view())

]
