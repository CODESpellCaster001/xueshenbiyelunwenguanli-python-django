from django.urls import path, include
from django.conf.urls import url
from apps.open_topic import views

urlpatterns = [
    path('upload_open_topic/', views.upload_open_topic, name="upload_open_topic"),
    path('download_open_topic/', views.download_open_topic, name="download_open_topic"),
]