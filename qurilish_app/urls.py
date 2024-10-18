from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', PostAPIView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('post/<slug:slug>/update', PostUpdateAPIView.as_view(), name='post_update'),
    path('auth/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('change_password/', PasswordChangeApiView.as_view(), name='change_password'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
