from django.urls import path, include
from django.conf.urls import url
from apps.topic_record import views

urlpatterns = [
    path('index/', views.all_topic, name="all_topic"),
    path('my_topic/', views.my_topic, name="my_topic"),
    path('create/', views.create_topic, name="create_topic"),
    url(r'^delete-(\d+)/$', views.delete_topic, name="delete_topic"),
    url(r'^edit-(\d+)/$', views.edit_topic, name="edit_topic"),
    url(r'^show-(\d+)/$', views.topic_detail, name="topic_detail"),
]