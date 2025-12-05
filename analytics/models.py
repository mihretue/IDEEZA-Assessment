from django.db import models
from django.utils import timezone


class User(models.Model):
    """User model for blog authors and viewers"""
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.username


class Country(models.Model):
    """Country model for geographic data"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # ISO 3166-1 alpha-2/3
    
    class Meta:
        db_table = 'countries'
        verbose_name_plural = 'countries'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Blog(models.Model):
    """Blog post model"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blogs',
        db_index=True
    )
    country = models.ForeignKey(
        Country, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='blogs',
        db_index=True
    )
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        db_table = 'blogs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['country', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title


class BlogView(models.Model):
    """Blog view/analytics tracking model"""
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name='views',
        db_index=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='blog_views',
        db_index=True
    )
    country = models.ForeignKey(
        Country, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='blog_views',
        db_index=True
    )
    viewed_at = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        db_table = 'blog_views'
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['blog', 'viewed_at']),
            models.Index(fields=['user', 'viewed_at']),
            models.Index(fields=['country', 'viewed_at']),
            models.Index(fields=['viewed_at']),
            # Composite indexes for common query patterns
            models.Index(fields=['blog', 'country', 'viewed_at']),
            models.Index(fields=['blog', 'user', 'viewed_at']),
        ]
    
    def __str__(self):
        return f"View of {self.blog.title} at {self.viewed_at}"

