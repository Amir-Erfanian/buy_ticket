from django.contrib import admin
from .models import BlogPost, Category



class PostAdmin(admin.ModelAdmin):
    empty_value_diplay = '-emtpy-'
    list_display = ('title', 'author', 'view_count', 'is_active')
    list_filter = ('is_active', 'author')
    search_fields = ('title', 'content')



admin.site.register(Category)
admin.site.register(BlogPost, PostAdmin)