from django.shortcuts import render
from django.http import JsonResponse
from django.core import mail
from django.conf import settings
from django.views.generic import TemplateView, ListView
from django.core.mail import EmailMessage

from .models import Post


class IndexView(TemplateView):
    template_name = "index.html"


class BlogView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog.html"


def contact(request):
    name = request.POST.get("name")
    email_address = request.POST.get("email_address")
    message = request.POST.get("message")
    message = email_address + "\n\n" + message
    print(name, email_address, message)
    if name and email_address and message:
        msg = EmailMessage(
            f"Contact from Personal Site - {name}",
            message,
            to=['ngenovictor321@gmail.com'])
        msg.send()
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "error"})


def journey(request):
    template = "journey.html"
    context = {
        "title": "Journey"
    }
    return render(request, template, context)
