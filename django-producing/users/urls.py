from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    path('registration/', views.register, name='registration'),
    path('auth/', auth_views.LoginView.as_view(
        template_name='users/auth.html'), name='auth')
]
