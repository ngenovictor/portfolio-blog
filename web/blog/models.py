from django.db import models

# Create your models here.
class Post(models.Model):
    """
    will hold details about a blogpost
    """
    slug = models.SlugField(unique=True)
    title = models.TextField()
    image = models.TextField()
    summary = models.TextField()
    content = models.TextField()
    draft = models.BooleanField(default=True)
    date_created = models.TimeField(auto_now_add=True)
    date_updated = models.TimeField(auto_now=True)

    def __str__(self):
        return self.title
