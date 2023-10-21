from django.urls import path
from .       import views
from .views import SignUpView, SignInView

urlpatterns = [
    path('', views.index, name='index'),
    path('/signUp', SignUpView.as_view()),
    path('/signIn', SignInView.as_view())
]