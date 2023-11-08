from django.urls import path
from .views      import *

urlpatterns = [
    path('', index, name='index'),
    path('/signUp', SignUpView.as_view()),
    path('/signIn', SignInView.as_view()),
    path('/kakao/login/', kakao_login, name='kakao_login'),
    path('/kakao/callback/', kakao_callback, name='kakao_callback'),
]