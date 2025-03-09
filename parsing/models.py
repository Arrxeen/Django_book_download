from django.db import models
from django.contrib.auth.models import User

class WebBook(models.Model):
    title = models.CharField(max_length=255)
    url_first = models.URLField()
    urls_parents = models.URLField()
    imga = models.URLField()
    creater = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=255)
    content = models.JSONField(default=list)
    book = models.ForeignKey(WebBook, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return self.title