from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # ✅ AI fields
    summary = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)

    # optional
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title