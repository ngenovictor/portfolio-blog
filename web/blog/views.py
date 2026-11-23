from django.views.generic import TemplateView, ListView, DetailView

from .models import Post


class IndexView(TemplateView):
    template_name = "index.html"


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


class PostDetailView(VisiblePostsMixin, DetailView):
    context_object_name = 'post'
    template_name = "post_detail.html"
