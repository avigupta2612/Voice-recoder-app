from django.db import models
from demoapp.models import User
from django.utils.text import slugify

# Create your models here.
class AudioFile(models.Model):
    input_audio = models.FileField(upload_to='input-audio')
    clean_audio = models.FileField(upload_to='clean-audio')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)

    def __str__(self):
        return self.id
    
    def save(self, **kwargs):
        self.slug = slugify(str(self.id), allow_unicode=True)
        super().save(**kwargs)

class Speech2Text(models.Model):
    input_audio = models.FileField(upload_to='s2t_audio')
    #clean_audio = models.FileField(upload_to='clean-audio')
    #userId = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null=True)

    def __str__(self):
        return self.id
    
    def save(self, **kwargs):
        self.slug = slugify(str(self.id), allow_unicode=True)
        super().save(**kwargs)