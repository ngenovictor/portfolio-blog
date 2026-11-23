from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


def make_post(title, draft):
    return Post.objects.create(title=title, image="", summary="s", content="c", draft=draft)


class DraftVisibilityTests(TestCase):
    def test_only_drafts_shows_empty_message_to_visitors(self):
        make_post("Hidden draft", draft=True)
        response = self.client.get(reverse("blog"))
        self.assertContains(response, "Watch out for posts later")
        self.assertNotContains(response, "Hidden draft")

    def test_published_posts_listed_without_empty_message(self):
        make_post("Published post", draft=False)
        make_post("Hidden draft", draft=True)
        response = self.client.get(reverse("blog"))
        self.assertContains(response, "Published post")
        self.assertNotContains(response, "Hidden draft")
        self.assertNotContains(response, "Watch out for posts later")

    def test_superuser_sees_drafts(self):
        get_user_model().objects.create_superuser("boss", "", "pw")
        self.client.login(username="boss", password="pw")
        post = make_post("Hidden draft", draft=True)
        self.assertContains(self.client.get(reverse("blog")), "Hidden draft")
        self.assertEqual(self.client.get(reverse("post_detail", args=[post.slug])).status_code, 200)

    def test_draft_detail_is_404_for_visitors(self):
        post = make_post("Hidden draft", draft=True)
        self.assertEqual(self.client.get(reverse("post_detail", args=[post.slug])).status_code, 404)


import json
import re

from django.test import override_settings


def meta(html, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', html)
    return m.group(1) if m else None


def ld_graph(html):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return json.loads(m.group(1))["@graph"]


@override_settings(SITE_URL="https://www.example.com")
class SeoTests(TestCase):
    def test_home_has_social_preview_tags(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertEqual(meta(html, "property", "og:url"), "https://www.example.com/")
        self.assertEqual(meta(html, "property", "og:type"), "profile")
        self.assertTrue(meta(html, "property", "og:image").startswith("https://www.example.com/static/"))
        self.assertEqual(meta(html, "property", "og:image:width"), "1200")
        self.assertEqual(meta(html, "name", "twitter:card"), "summary_large_image")
        self.assertIn('<link rel="canonical" href="https://www.example.com/">', html)
        types = {item["@type"] for item in ld_graph(html)}
        self.assertEqual(types, {"Person", "WebSite", "ProfilePage"})

    def test_blog_canonical_ignores_tracking_query(self):
        html = self.client.get(reverse("blog") + "?utm_source=x").content.decode()
        self.assertIn('<link rel="canonical" href="https://www.example.com/blog">', html)
        self.assertTrue(meta(html, "property", "og:image"))

    def test_post_tags_use_absolute_image_and_safe_json_ld(self):
        post = Post.objects.create(
            title='Tricky </script> "title"', image="/static/img/x.png",
            summary="sum", content="c", draft=False,
        )
        html = self.client.get(post.get_absolute_url()).content.decode()
        self.assertEqual(meta(html, "property", "og:type"), "article")
        self.assertEqual(meta(html, "property", "og:image"), "https://www.example.com/static/img/x.png")
        posting = next(i for i in ld_graph(html) if i["@type"] == "BlogPosting")
        self.assertEqual(posting["headline"], 'Tricky </script> "title"')
        self.assertEqual(posting["url"], "https://www.example.com" + post.get_absolute_url())

    def test_sitemap_lists_published_posts_only(self):
        published = make_post("Published post", draft=False)
        draft = make_post("Hidden draft", draft=True)
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("<loc>https://www.example.com/</loc>", xml)
        self.assertIn("<loc>https://www.example.com/blog</loc>", xml)
        self.assertIn("https://www.example.com" + published.get_absolute_url(), xml)
        self.assertNotIn(draft.get_absolute_url(), xml)

    def test_robots_txt_points_to_sitemap(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Sitemap: https://www.example.com/sitemap.xml")
