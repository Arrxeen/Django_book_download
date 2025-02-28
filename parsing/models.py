from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class WebBook(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    creater = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='parsers')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('task-detail', kwargs = {'pk': self.pk})


class Chapter(models.Model):
    book = models.ForeignKey(WebBook, on_delete=models.CASCADE, related_name='chapters')
    falls_id = models.TextField(null=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title