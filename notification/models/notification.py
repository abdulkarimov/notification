from django.db import models

from .template import Template
from .sendmethod import SendMethod


class Notification(models.Model):
    __tablename__ = "Notification"
    params = models.CharField(max_length=255)
    date = models.DateField()
    templateID = models.ForeignKey(Template, on_delete=models.CASCADE)
    sendMethodID = models.ForeignKey(SendMethod, on_delete=models.CASCADE)




