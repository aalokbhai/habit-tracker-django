from django.db import models
from django.utils.timezone import localdate
from django.contrib.auth.models import User

class task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    task_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.task_name

class TaskProgress(models.Model):
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    date = models.DateField(default=localdate)
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('task', 'date')
        ordering = ['-date']

# New model for about page content
class AboutContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True, help_text="URL for feature image")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
# Simple model with only 3 fields
from django.db import models

class Social(models.Model):
    platform_name = models.CharField(max_length=100, blank=True, null=True)
    platform_url = models.URLField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Social'

    def __str__(self):
        return self.platform_name