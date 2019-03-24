from django.urls import path, include
from django.conf.urls import include
from .views import (UserCreateAPIView, LoginAPIView, RReadingAPIView, RReadingListAPIView)

urlpatterns = [

    path('register/', UserCreateAPIView.as_view(), name='user_register'),

    path('login/', LoginAPIView.as_view(), name='user_login'),

    path('readinglist/', RReadingListAPIView.as_view(), name='readinglist'),
    path('reading/', RReadingAPIView.as_view(), name='reading'),
]