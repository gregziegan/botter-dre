from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

class Lyrics(models.Model):
    words = models.TextField(unique=True)


class GeneratedSong(models.Model):
    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    created_by = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateField(default=datetime.now())
