from django.urls import path, include
from django.conf.urls import url
from apps.user import views

urlpatterns = [
    path('user_center/', views.user_center, name='user_center'),
    path('edit_user_profile/', views.edit_user_profile, name="edit_user_profile"),
    path('change_pwd/', views.change_pwd, name="change_pwd"),
]