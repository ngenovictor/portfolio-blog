from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class SiteUrlSitemap(Sitemap):
    """Build sitemap URLs from SITE_URL rather than the request host."""

    def get_domain(self, site=None):
        return urlsplit(settings.SITE_URL).netloc

    def get_protocol(self, protocol=None):
        return urlsplit(settings.SITE_URL).scheme


class StaticViewSitemap(SiteUrlSitemap):
    def items(self):
        return ["home", "blog"]

    def location(self, item):
        return reverse(item)


class PostSitemap(SiteUrlSitemap):
    def items(self):
        return Post.objects.filter(draft=False).order_by("-date_created")

    def lastmod(self, post):
        return post.date_updated


sitemaps = {"static": StaticViewSitemap, "posts": PostSitemap}
