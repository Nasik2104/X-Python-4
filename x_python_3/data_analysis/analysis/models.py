import os

from django.db import models
from django.contrib.auth import settings
from django.core.exceptions import ValidationError


class FileStorage(models.Model):
    TYPE_CHOICES = {
        'csv':'CSV',
    }

    type = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES
    )
    file = models.FileField(upload_to='files/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        file_end = os.path.splitext(self.file.name)[1].lower()
        if file_end == '.csv':
            self.type = 'csv'
        else:
            raise ValidationError(f'Files type {file_end} is not supported.')
        super().save(*args, **kwargs)


class History(models.Model):
    file = models.ForeignKey(FileStorage, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='history')
    column = models.CharField(max_length=128, null=True, blank=True)
    condition = models.CharField(max_length=3, null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    column_2 = models.CharField(max_length=128, null=True, blank=True)
    search = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
