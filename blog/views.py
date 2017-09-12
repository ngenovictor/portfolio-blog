from django.shortcuts import render


def index(request):
    template ="index.html"
    context = {
        "title":"Home"
    }
    return render(request, template, context)
