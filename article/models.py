from django.db import models
from django.conf import settings

from category.models import Category
# Create your models here.


class Article(models.Model):
    STATUS_CHOICES = [
        ('PUBLIC', 'Public'),
        ('SECRET', 'Secret')
    ]

    url_address = models.CharField(max_length=300)
    title = models.CharField(max_length=300, blank=True, null=True)
    image = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    file_url = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='SECRET')
    category = models.ForeignKey(Category,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = 'article'


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)
