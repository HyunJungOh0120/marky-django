from django.urls import path

from .views import (ChangePasswordView, CookieTokenRefreshView, LoginView,
                    LogoutView, RegisterView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='token_obtain'),
    path('login/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/<int:pk>',
         ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout')
]
