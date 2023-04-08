from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('blog', views.BlogView.as_view(), name="blog"),
    path('journey', views.journey, name="journey"),
    path('contact', views.contact, name="contact")
]
