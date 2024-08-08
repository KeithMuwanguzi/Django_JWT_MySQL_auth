from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signUp),
    path('login/',views.login),
    path('users/',views.getUsers),
]