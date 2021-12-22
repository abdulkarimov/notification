import telepot
import telegram_send
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from notification.models import Notification, Template, SendMethod
from notification.serializers import NotificationSerializer, TemplateSerializer, SendMethodSerializer
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
import json


@permission_classes((permissions.AllowAny,))
class NotificationView(APIView):
    def get(self, request):
        notification = Notification.objects.all()
        serializer = NotificationSerializer(instance=notification, many=True)

        return Response({"notification": serializer.data})

    def post(self, request):
        # notificationData = request.data.get('notification')
        # serializer = NotificationSerializer(data=notificationData)
        # serializer.date = datetime.datetime.today().strftime('%d-%m-%Y / %H:%M')

        data = json.loads(request.body.decode('utf-8'))['notification']
        params = data['params']
        template = data['templateID_id']
        sendMethod = data['sendMethodID_id']

        notification = Notification(params=params, templateID=Template.objects.get(id=template), sendMethodID=SendMethod.objects.get(id=sendMethod))
        template = Template.objects.get(id=notification.templateID.id)
        text = template.text.replace('#', notification.params)

        if notification.sendMethodID.id == 1:
            email = EmailMessage(template.name, text, to=['sniper123zoom@gmail.com'])
            email.send()
        elif notification.sendMethodID.id == 2:
            # https://telepot.readthedocs.io/en/latest/
            bot = telepot.Bot('5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8')
            bot.sendMessage(861921150, text)#id key from chat https://api.telegram.org/bot5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8/getUpdates
            # telegram_send.send(messages=["Wow that was easy!"])

        notification.save()
        return JsonResponse(model_to_dict(notification))


        # if serializer.is_valid(raise_exception=True):
        #     notification = serializer.save()
        #
        # id = notification.templateID
        # id = int(id.id)
        #
        # template = Template.objects.get(id=id).text
        # template = template.replace('#', notification.params)
        # email = EmailMessage(serializer.date, template, to=['sniper123zoom@gmail.com'])
        # email.send()
        #
        # return JsonResponse(model_to_dict(notification))

    def put(self, request, pk):
        saved_notification = get_object_or_404(Notification.objects.all(), pk=pk)
        data = request.data.get('notification')
        serializer = NotificationSerializer(instance=saved_notification, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_notification = serializer.save()
        return JsonResponse(model_to_dict(saved_notification))

    def delete(self, request, pk):
        # Get object with this pk
        notification = get_object_or_404(Notification.objects.all(), pk=pk)
        notification.delete()
        return Response({
            "message": "Notification with id {} has been deleted.".format(pk)
        }, status=204)


@permission_classes((permissions.AllowAny,))
class TemplateView(APIView):
    def get(self, request):
        template = Template.objects.all()
        serializer = TemplateSerializer(instance=template, many=True)
        return Response({"template": serializer.data})

    def post(self, request):
        templateData = request.data.get('template')
        serializer = TemplateSerializer(data=templateData)
        if serializer.is_valid(raise_exception=True):
            template = serializer.save()
        return JsonResponse(model_to_dict(template))

    def put(self, request, pk):
        saved_template = get_object_or_404(Template.objects.all(), pk=pk)
        data = request.data.get('template')
        serializer = TemplateSerializer(instance=saved_template, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_template = serializer.save()
        return JsonResponse(model_to_dict(saved_template))

    def delete(self, request, pk):
        # Get object with this pk
        template = get_object_or_404(Template.objects.all(), pk=pk)
        template.delete()
        return Response({
            "message": "Notification with id {} has been deleted.".format(pk)
        }, status=204)


@permission_classes((permissions.AllowAny,))
class SendMethodView(APIView):
    def get(self, request):
        sendMethod = SendMethod.objects.all()
        serializer = SendMethodSerializer(instance=sendMethod, many=True)
        return Response({"sendMethod": serializer.data})

    def post(self, request):
        sendMethodData = request.data.get('sendMethod')
        serializer = SendMethodSerializer(data=sendMethodData)
        if serializer.is_valid(raise_exception=True):
            sendMethod = serializer.save()
        return JsonResponse(model_to_dict(sendMethod))

    def put(self, request, pk):
        saved_sendMethod = get_object_or_404(Template.objects.all(), pk=pk)
        data = request.data.get('sendMethod')
        serializer = SendMethodSerializer(instance=saved_sendMethod, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_sendMethod = serializer.save()
        return JsonResponse(model_to_dict(saved_sendMethod))

    def delete(self, request, pk):
        # Get object with this pk
        sendMethod = get_object_or_404(Template.objects.all(), pk=pk)
        sendMethod.delete()
        return Response({
            "message": "Notification with id {} has been deleted.".format(pk)
        }, status=204)
