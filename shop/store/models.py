from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logo = models.ImageField(upload_to='shop/', default="default-shop-logo.png", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'All Stores'
        ordering = ['created_at', 'name']
