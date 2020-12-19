from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profiles", null=True, blank=True)
    profession = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    


class Blog(models.Model):
    title = models.CharField( max_length=50)
    body = models.TextField()
    feature_image = models.ImageField(upload_to='feature_images')
    blogger = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    blogger = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    blogger = models.ForeignKey(User, on_delete=models.CASCADE)


    
