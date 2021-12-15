from django.db import models

#тип отправки(Мыло)
class SendMethod(models.Model):
    __tablename__ = "SendMethod"
    nameMethod = models.CharField(max_length=20)
