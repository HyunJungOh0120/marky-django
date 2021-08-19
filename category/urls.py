from django.urls import path

from category.views import CategoriesAPIView, CategoryAPIView

urlpatterns = [
    path('', CategoriesAPIView.as_view()),
    path('<int:id>', CategoryAPIView.as_view()),

]
