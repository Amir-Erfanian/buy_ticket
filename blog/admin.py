from django.contrib import admin
from .models import BlogPost, Category
from django_summernote.admin import SummernoteModelAdmin



class PostAdmin(SummernoteModelAdmin):
    empty_value_diplay = "-emtpy-"
    list_display = ("title", "author", "view_count", "is_active")
    list_filter = ("is_active", "author")
    search_fields = ("title", "content")
    summernote_fields = ('content',)


admin.site.register(Category)
admin.site.register(BlogPost, PostAdmin)
