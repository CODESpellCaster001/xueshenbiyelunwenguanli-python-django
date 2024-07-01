"""Graduation_design_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from apps.user.views import RegisterView, LoginView, LogoutView
from apps.user import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^topic/', include(('apps.topic_record.urls', 'apps.topic_record'), namespace='topic')),
    url(r'^choose_topic/', include(('apps.choose_topic.urls', 'apps.choose_topic'), namespace='choose_topic')),
    url(r'^open_topic/', include(('apps.open_topic.urls', 'apps.open_topic'), namespace='open_topic')),
    url(r'^middle_topic/', include(('apps.middle_topic.urls', 'apps.middle_topic'), namespace='middle_topic')),
    url(r'^defense/', include(('apps.defense.urls', 'apps.defense'), namespace='defense')),
    url(r'^score_feedback/', include(('apps.score_feedback.urls', 'apps.score_feedback'), namespace='score_feedback')),
    url(r'^user/', include(('apps.user.urls', 'apps.user'), namespace='user')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
handler404 = views.page_not_found
handler500 = views.page_error
