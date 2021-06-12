from django.db import models
from demoapp.models import User
# Create your models here.
class AudioFile(models.Model):
    input_audio = models.FileField(upload_to='input-audio')
    clean_audio = models.FileField(upload_to='clean-audio')
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userId