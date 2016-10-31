from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^profile/$', views.index, name='index'),
]