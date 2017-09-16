from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^blog$', views.view_blog_site, name="blog"),
]
