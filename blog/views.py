from django.shortcuts import render
from django.http import JsonResponse
from django.core import mail
from django.conf import settings
from django.views.generic import TemplateView, ListView

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
    if name and email_address and message:
        mail.send_mail(
            subject="Contact from Personal Site - {0}".format(name),
            from_email=email_address,
            recipient_list=[settings.EMAIL_HOST_USER, 'ngenovictor321@gmail.com'],
            fail_silently=False,
            message=message,
        )
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "error"})

def journey(request):
    template = "journey.html"
    context = {
        "title": "Journey"
    }
    return render(request, template, context)