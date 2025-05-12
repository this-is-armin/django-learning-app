from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='course/images/', validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def detail(self):
        return reverse('course:one', args=[self.slug])
    
    def course_save(self):
        return reverse('course:save', args=[self.slug])
    
    def course_un_save(self):
        return reverse('course:un-save', args=[self.slug])


class Episode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='episodes')
    counter = models.PositiveBigIntegerField()
    description = models.TextField()
    video = models.FileField(upload_to='course/episode/videos/', validators=[FileExtensionValidator(['mp4', 'mkv'])])
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['counter']
    
    def __str__(self):
        return f"episode: {self.counter} - course: {self.course.title}"
    
    def detail(self):
        return reverse('course:episode', args=[self.course.slug, self.counter])


class Comment(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name
    

class CourseSave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.course.title