"""youtube_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from youtube import views as youtube_view
import oauth2client.contrib.django_util.site as django_util_site

urlpatterns = [
	url(r'^$', youtube_view.index),
	url(r'^oauth2/', include(django_util_site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', auth_views.login, name='login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/', auth_views.logout, name='logout',
        kwargs={'next_page': '/login'}),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^youtube/', include('youtube.urls')),
    url(r'^profile_required$', youtube_view.get_profile_required),
    url(r'^profile_enabled$', youtube_view.get_profile_optional),
]
