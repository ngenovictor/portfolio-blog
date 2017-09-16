from django.shortcuts import render


def index(request):
    template ="index.html"
    context = {
        "title":"Home"
    }
    return render(request, template, context)


def view_blog_site(request):
    template = "blog.html"
    context = {
        "title":"Veekay Blog"
    }
    return render(request, template, context)