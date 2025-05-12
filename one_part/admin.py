from django.contrib import admin
from .models import OnePart, Comment, OnePartSave


@admin.register(OnePart)
class OnePartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_published', 'created', 'updated']
    list_filter = ['user', 'title', 'is_published']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'one_part', 'name', 'is_published', 'created']
    list_filter = ['one_part', 'name', 'is_published']
    search_fields = ['comment']


@admin.register(OnePartSave)
class OnePartSaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'one_part', 'created']
    list_filter = ['user', 'one_part']
    search_fields = ['one_part']