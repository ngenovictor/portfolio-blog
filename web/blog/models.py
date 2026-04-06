from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    """
    will hold details about a blogpost
    """
    slug = models.SlugField(unique=True, blank=True)
    title = models.TextField()
    image = models.TextField()
    summary = models.TextField()
    content = models.TextField()
    draft = models.BooleanField(default=True)
    date_created = models.TimeField(auto_now_add=True)
    date_updated = models.TimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
