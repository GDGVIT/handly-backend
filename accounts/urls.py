from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('create/',views.UserSignupView.as_view()),
    path('login/',views.UserLoginView.as_view()),   
]