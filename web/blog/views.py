from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, ListView, DetailView

from . import seo
from .models import Post


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seo"] = seo.page_meta(
            title="Victor Ng'eno — Software Engineer",
            description=seo.SITE_DESCRIPTION,
            path=reverse("home"),
            og_type="profile",
        )
        context["structured_data"] = seo.with_context(
            seo.person(),
            seo.website(),
            {
                "@type": "ProfilePage",
                "@id": settings.SITE_URL + "/#profile",
                "url": settings.SITE_URL + "/",
                "name": "Victor Ng'eno — Software Engineer",
                "mainEntity": {"@id": settings.SITE_URL + "/#person"},
                "isPartOf": {"@id": settings.SITE_URL + "/#website"},
            },
        )
        return context


class VisiblePostsMixin:
    """Drafts are visible to superusers only; everyone else gets published posts."""

    def get_queryset(self):
        posts = Post.objects.order_by("-date_created")
        if not self.request.user.is_superuser:
            posts = posts.filter(draft=False)
        return posts


class BlogView(VisiblePostsMixin, ListView):
    context_object_name = 'posts'
    template_name = "blog.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = reverse("blog")
        page = context["page_obj"].number if context.get("is_paginated") else 1
        if page > 1:
            path += f"?page={page}"
        context["seo"] = seo.page_meta(
            title="Blog — Victor Ng'eno",
            description=seo.BLOG_DESCRIPTION,
            path=path,
        )
        blog_url = seo.absolute_url(reverse("blog"))
        context["structured_data"] = seo.with_context(
            seo.person(),
            {
                "@type": "Blog",
                "@id": blog_url + "#blog",
                "name": "Blog — Victor Ng'eno",
                "description": seo.BLOG_DESCRIPTION,
                "url": blog_url,
                "author": {"@id": settings.SITE_URL + "/#person"},
                "blogPost": [seo.blog_posting(post) for post in context["posts"] if not post.draft],
            },
        )
        return context


class PostDetailView(VisiblePostsMixin, DetailView):
    context_object_name = 'post'
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["post"]
        context["seo"] = seo.page_meta(
            title=post.title,
            description=post.summary,
            path=post.get_absolute_url(),
            og_type="article",
            image=seo.post_image(post),
            robots="noindex, nofollow" if post.draft else "index, follow",
            author_url=settings.SITE_URL + "/",
            published=post.date_created,
            modified=post.date_updated,
        )
        context["structured_data"] = seo.with_context(seo.person(), seo.blog_posting(post))
        return context


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "",
        f"Sitemap: {settings.SITE_URL}{reverse('sitemap')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
