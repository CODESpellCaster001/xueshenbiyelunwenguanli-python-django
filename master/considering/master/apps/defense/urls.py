from django.urls import path, include
from django.conf.urls import url
from apps.defense import views

urlpatterns = [
    # path('upload_graduation_topic/', views.upload_graduation_topic, name="upload_graduation_topic"),
    path('waiting_for_confirm_defense/', views.waiting_for_confirm_defense, name="waiting_for_confirm_defense"),
    path('student_list/', views.student_list, name="student_list"),
    url(r'^confirm_(\d+)/$', views.confirm_defense, name='confirm_defense'),
    url(r'^upload_graduation_topic-(\d+)/$', views.upload_graduation_topic, name="upload_graduation_topic"),

]