from typing_extensions import Required
from django.db import models
from django.db.models.fields.related import ForeignKey
from user.models import MyUser
# Create your models here.


class Article(models.Model):
    STATUS_CHOICES = [
        ('PUBLIC', 'Public'),
        ('SECRET', 'Secret')
    ]

    url_address = models.CharField(required=True)
    title = models.CharField(blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='SECRET')
    category = models.ForeignKey(null=True, blank=True)  # TODO
