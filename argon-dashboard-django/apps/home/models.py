# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to='files')
    def __str__(self):
        return self.file.name