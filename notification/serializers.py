from rest_framework import serializers
from .models import Notification, Template, SendMethod

class NotificationSerializer(serializers.Serializer):

    params = serializers.CharField(max_length=255)
    # date = serializers.DateField(
    # format = '%d.%m.%Y',
    # input_formats=['%d.%m.%Y', 'iso-8601', '1'])
    templateID_id = serializers.IntegerField()
    sendMethodID_id = serializers.IntegerField()

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.params = validated_data.get('params', instance.params)
        instance.date = validated_data.get('date', instance.date)
        instance.templateID_id = validated_data.get('templateID_id', instance.templateID_id)
        instance.sendMethodID_id = validated_data.get('sendMethodID_id', instance.sendMethodID_id)
        instance.save()
        return instance


class TemplateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    text = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Template.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.text)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class SendMethodSerializer(serializers.Serializer):
    nameMethod = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return SendMethod.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nameMethod = validated_data.get('nameMethod', instance.nameMethod)
        instance.save()
        return instance


