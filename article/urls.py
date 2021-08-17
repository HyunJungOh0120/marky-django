from django.urls import path
from .views import ArticlePostUrl


urlpatterns = [
    path('', ArticlePostUrl.as_view())
]
