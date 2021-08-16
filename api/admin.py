from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Category)


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'created_by', 'category')
    list_filter = ("created", )
    search_fields = ['title', 'category']
    summernote_fields = ('body', )


admin.site.register(Post, PostAdmin)
