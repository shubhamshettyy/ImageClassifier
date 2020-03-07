from django.db import models

# Create your models here.


class Image(models.Model):
    zipped_images = models.FileField(upload_to='uploads/')
