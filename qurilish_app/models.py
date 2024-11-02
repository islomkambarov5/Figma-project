from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.
from django.urls import reverse


class Posts(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=255, verbose_name='Title')
    context = models.TextField(verbose_name='Description')
    comments = models.ManyToManyField(User, through='Comments', related_name='post_comments', blank=True,
                                      verbose_name='Comments')
    # views = models.IntegerField(default=0, verbose_name='Views')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Author')
    slug = models.SlugField(null=True, blank=True, unique=True)
    # likes = models.ManyToManyField(User, related_name='post_likes', blank=True, verbose_name='Likes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at', '-likes']
        indexes = [
            models.Index(fields=['-created_at']),
        ]


class Comments(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    text = models.TextField(verbose_name='Comment text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Post', related_name='post_comments')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]


class Likes(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Post', related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'
    
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
