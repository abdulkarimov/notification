from django.db import models

# шаблон для сообщений
class Template(models.Model):
    __tablename__ = "Template"
    text = models.CharField(max_length=255)
