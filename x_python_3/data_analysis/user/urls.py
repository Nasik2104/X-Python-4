from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('register/', views.UserRegister.as_view(), name='user-register'),
    path('profile/', views.UserProfile.as_view(), name='user-profile')
]