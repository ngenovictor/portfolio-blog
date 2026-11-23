from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import sitemaps

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("blog", views.BlogView.as_view(), name="blog"),
    path("blog/<slug:slug>", views.PostDetailView.as_view(), name="post_detail"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
