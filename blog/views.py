from django.shortcuts import render
from django.http import JsonResponse
from django.core import mail
from django.conf import settings

def index(request):
    template ="index.html"
    context = {
        "title":"Home"
    }
    return render(request, template, context)


def contact(request):
    name = request.POST.get("name")
    email_address = request.POST.get("email_address")
    message = request.POST.get("message")
    if name and email_address and message:
        mail.send_mail(
            subject="Contact from Personal Site",
            from_email=email_address,
            recipient_list=[settings.EMAIL_HOST_USER, 'ngenovictor321@gmail.com'],
            fail_silently=False,
            message=message,
            html_message=message,
        )
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "error"})



def view_blog_site(request):
    template = "blog.html"
    context = {
        "title":"Veekay Blog"
    }
    return render(request, template, context)