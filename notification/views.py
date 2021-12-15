from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from notification.models import Notification
from notification.serializers import NotificationSerializer


@permission_classes((permissions.AllowAny,))
class NotificationView(APIView):
    def get(self, request):
        notification = Notification.objects.all()
        return Response({"notification": notification})
    def post(self , request):
        notificationData = request.data.get('notification')
        serializer = NotificationSerializer(data=notificationData)
        if serializer.is_valid(raise_exception=True):
            notification = serializer.save()
        return Response({notification})