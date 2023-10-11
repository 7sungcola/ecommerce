from django.urls import path
from users.views import *

urlpatterns = [
    path('/signUp', SignUpView.as_view()),
    path('/signIn', SignInView.as_view())
]