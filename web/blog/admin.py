from django.contrib import admin

from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'draft')
    list_display_links = ('slug',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
