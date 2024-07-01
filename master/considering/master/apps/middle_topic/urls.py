from django.urls import path, include
from django.conf.urls import url
from apps.middle_topic import views

urlpatterns = [
    path('upload_middle_topic/', views.upload_middle_topic, name="upload_middle_topic"),
    path('download_middle_topic/', views.download_middle_topic, name="download_middle_topic"),
]