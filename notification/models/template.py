from django.db import models

# шаблон для сообщений
class Template(models.Model):
    __tablename__ = "Template"
    name = models.CharField(max_length=255, default='Template')
    text = models.CharField(max_length=255)
