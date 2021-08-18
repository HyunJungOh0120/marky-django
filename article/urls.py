from django.urls import path
from .views import ArticleAPIView, OneArticleAPIView, GetPdfView


urlpatterns = [
    path('', ArticleAPIView.as_view()),
    path('pdf/', GetPdfView.as_view()),
    path('<int:id>', OneArticleAPIView.as_view()),

]
