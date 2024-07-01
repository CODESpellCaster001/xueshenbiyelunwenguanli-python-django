from django.urls import path, include
from django.conf.urls import url
from apps.score_feedback import views

urlpatterns = [
    path('get_score_set_feedback/', views.get_score_set_feedback, name="get_score_set_feedback"),
    # path('set_score_set_feedback/', views.set_score_set_feedback, name="set_score_set_feedback"),
    url(r'set_score_set_feedback-(\d+)/$', views.set_score_set_feedback, name="set_score_set_feedback"),

    path('waiting_for_score/', views.waiting_for_score, name="waiting_for_score"),
    path('my_feedback/', views.my_feedback, name="my_feedback"),
    # path('download_open_topic/', views.download_open_topic, name="download_open_topic"),
]