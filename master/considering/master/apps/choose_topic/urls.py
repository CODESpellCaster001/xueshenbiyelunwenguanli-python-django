from django.urls import path, include
from django.conf.urls import url
from apps.choose_topic import views

urlpatterns = [
    path('show_chosen_topic/', views.show_chosen_topic, name="show_chosen_topic"),
    url(r'^choose_(\d+)/$', views.choose_topic, name="choose_topic"),
    url(r'^confirm_(\d+)/$', views.confirm_choose_topic, name='confirm_choose_topic'),
    path('show_waiting_for_confirm_choose_topic/', views.show_waiting_for_confirm_choose_topic,
         name="show_waiting_for_confirm_choose_topic"),

]