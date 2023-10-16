from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('users', include('users.urls')),
    path('posts', include('posts.urls'))
]
