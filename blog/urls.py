from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="home"),
    url(r'^blog$', views.BlogView.as_view(), name="blog"),
    url(r'^journey$', views.journey, name="journey"),
    url(r'^contact', views.contact, name="contact")
]
