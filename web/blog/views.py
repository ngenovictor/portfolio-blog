from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from .models import Post


class IndexView(TemplateView):
    template_name = "index.html"


class BlogView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog.html"
    paginate_by = 20


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "post_detail.html"


def journey(request):
    template = "journey.html"
    context = {
        "title": "Journey"
    }
    return render(request, template, context)
