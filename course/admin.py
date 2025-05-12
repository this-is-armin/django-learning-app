from django.contrib import admin
from .models import Course, Episode, Comment, CourseSave


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_published', 'created', 'updated']
    list_filter = ['user', 'title', 'is_published']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'counter', 'is_published', 'created', 'updated']
    list_filter = ['user', 'course', 'is_published']
    search_fields = ['description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'episode', 'name', 'is_published', 'created']
    list_filter = ['episode', 'name', 'is_published']
    search_fields = ['comment']


@admin.register(CourseSave)
class CourseSaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'created']
    list_filter = ['user', 'course']
    search_fields = ['course']