from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Posts(models.Model):
    # objects = models.Manager

    title = models.CharField(max_length=255, verbose_name='Title')
    context = models.TextField(verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Author')
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    text = models.TextField(verbose_name='Comment text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Post')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

