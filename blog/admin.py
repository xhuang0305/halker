from django.contrib import admin
from .models import Post, Category, Tag
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
class PostAdmin(MarkdownxModelAdmin):
    list_display = ['title', 'created', 'modified', 'category', 'author']

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)