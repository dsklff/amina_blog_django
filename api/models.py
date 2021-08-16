from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Nurgul(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    education = models.CharField(max_length=50)


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    author = models.CharField(max_length=250)
    body = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'id: {} and comment: {}'.format(self.id, self.body)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.id)


