from django.urls import include, path
from .views import FileUploadView


urlpatterns = [
    path('', FileUploadView.as_view())
]
