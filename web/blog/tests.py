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
