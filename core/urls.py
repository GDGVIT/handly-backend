from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('collections/',views.CollectionsView.as_view()),
    path('handwriter/',views.FileUploadView.as_view()),
    path('signed/',views.FileUploadPresignView.as_view()),
    path('view/',views.ViewFiles.as_view()),
    path('update/<pk>/',views.InputLoggerUpdate.as_view())
]