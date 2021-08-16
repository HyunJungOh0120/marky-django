
from django.db import models
from django.db.models.fields.related import ForeignKey
from user.models import MyUser
from category.models import Category
# Create your models here.


class Article(models.Model):
    STATUS_CHOICES = [
        ('PUBLIC', 'Public'),
        ('SECRET', 'Secret')
    ]

    url_address = models.CharField(max_length=300)
    title = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to='media/', null=True, blank=True)
    slug = models.SlugField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='SECRET')
    category = models.ForeignKey(Category,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)
