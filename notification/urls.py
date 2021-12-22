from django.urls import path, include
from notification.views import NotificationView, TemplateView, SendMethodView

app_name = 'notifications'
urlpatterns = [
    path('notifications/', NotificationView.as_view()),
    path('notifications/<int:pk>', NotificationView.as_view()),
    path('templates', TemplateView.as_view()),
    path('templates/<int:pk>', TemplateView.as_view()),
    path('sendMethod/', SendMethodView.as_view()),
    path('sendMethod/<int:pk>', SendMethodView.as_view())

]
