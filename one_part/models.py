from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse


class OnePart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='one_parts')
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    video = models.FileField(upload_to='one_part/videos/', validators=[FileExtensionValidator(['mp4', 'mkv'])])
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def detail(self):
        return reverse('one_part:one', args=[self.slug])
    
    def one_part_save(self):
        return reverse('one_part:one-part-save', args=[self.slug])
    
    def one_part_un_save(self):
        return reverse('one_part:one-part-un-save', args=[self.slug])
    

class Comment(models.Model):
    one_part = models.ForeignKey(OnePart, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name
        

class OnePartSave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_one_parts')
    one_part = models.ForeignKey(OnePart, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.one_part.title