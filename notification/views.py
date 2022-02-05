# pip install telepot --upgrade
import telepot
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
import requests
from time import sleep
import config
import telebot
from telebot import types

@permission_classes((permissions.AllowAny,))
class NotificationView(APIView):
    def get(self, request):
        notification = Notification.objects.all()
        serializer = NotificationSerializer(instance=notification, many=True)
        return Response({"notification": serializer.data})

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))['notification']
        params = data['params']
        template = data['templateID_id']
        sendMethod = data['sendMethodID_id']

        notification = Notification(params=params, templateID=Template.objects.get(id=template), sendMethodID=SendMethod.objects.get(id=sendMethod))
        template = Template.objects.get(id=notification.templateID.id)
        text = template.text

        for i in params:
            text = text.replace('#' + i, params[i])

        if notification.sendMethodID.id == 1:
            email = EmailMessage(template.name, text, to=['sniper123zoom@gmail.com'])
            email.send()
        elif notification.sendMethodID.id == 2:
            # https://telepot.readthedocs.io/en/latest/
            bot = telepot.Bot('5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8')
            bot.sendMessage(861921150, text)#id key from chat https://api.telegram.org/bot5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8/getUpdates
            update_id = bot.getUpdates()[-1]['update_id']
            while True:
                sleep(2)
                messages = bot.getUpdates(update_id)  # Получаем обновления
                for message in messages:
                    # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
                    if update_id < message['update_id']:
                        update_id = message['update_id']
                        text = f"ID пользователя: {message['message']['chat']['id']}, Сообщение: {message['message']['text']}"
                        bot.sendMessage(861921150, text)

        notification.save()

        id = notification.templateID
        id = int(id.id)

        template = Template.objects.get(id=id).text
        template = template.replace('#', notification.params)
        email = EmailMessage(serializer.date, template, to=['sniper123zoom@gmail.com'])
        email.send()

        return JsonResponse(model_to_dict(notification))

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
        saved_sendMethod = get_object_or_404(SendMethod.objects.all(), pk=pk)
        data = request.data.get('sendMethod')
        serializer = SendMethodSerializer(instance=saved_sendMethod, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_sendMethod = serializer.save()
        return JsonResponse(model_to_dict(saved_sendMethod))

    def delete(self, request, pk):
        # Get object with this pk
        sendMethod = get_object_or_404(SendMethod.objects.all(), pk=pk)
        sendMethod.delete()
        return Response({
            "message": "Notification with id {} has been deleted.".format(pk)
        }, status=204)

@permission_classes((permissions.AllowAny,))
class UsersView(APIView):
    def get(self, request , name):
        import collections
        url = 'https://api.telegram.org/bot5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8/getUpdates'
        r = requests.get(url)
        droplets = r.json()
        a = collections.defaultdict(list)

        for i in range(0,len(droplets['result'])):
            a[droplets['result'][i]['message']['chat']['first_name']] =droplets['result'][i]['message']['chat']['id']

        return Response(a.get(name))

@permission_classes((permissions.AllowAny,))
class GreenView(APIView):
    def post(self, request):
        text = json.loads(request.body.decode('utf-8'))['text']
        bot = telepot.Bot('5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8')
        bot.sendMessage(861921150, text)
        return Response("ok")

@permission_classes((permissions.AllowAny,))
class YellowView(APIView):
    def post(self, request):

        telebott = telebot.TeleBot('5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8')
        telepott = telepot.Bot('5004111173:AAGrkTPki8mSDRQUpNgU30WlmSCA8bw_dd8')
        text = json.loads(request.body.decode('utf-8'))['text']
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('YES')
        telebott.send_message(861921150, text)

        update_id = telepott.getUpdates()[-1]['update_id']

        f = False
        while True:
            messages = telepott.getUpdates(update_id)
            for message in messages:
                # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
                if update_id < message['update_id']:
                    update_id = message['update_id']
                    if message['message']['text'] == 'YES':
                        f = True
            if f:
                telebott.send_message(861921150, "ok")
                break
            else:
                telebott.send_message(861921150, 'вы приняли Сообщение?', reply_markup=keyboard)
                sleep(5)





        return Response("ok")







