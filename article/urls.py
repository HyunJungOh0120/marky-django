from django.urls import path
from .views import ArticleUploadUrl, FileUploadView


urlpatterns = [
    path('', ArticleUploadUrl.as_view()),
    path('upload/', FileUploadView.as_view())
]
