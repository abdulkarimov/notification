import datetime

import args as args
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.Serializer):
    params = serializers.CharField(max_length=255)
   # date = serializers.DateTimeField(*args, **kwargs)
    templateID_id = serializers.IntegerField()
    sendMethodID_id = serializers.IntegerField()
    def create(self, validated_data):
        return Notification.objects.create(**validated_data)