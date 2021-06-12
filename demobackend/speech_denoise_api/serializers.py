from rest_framework import serializers
from .models import AudioFile

class AudioFileModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioFile
        fields =('userId','input_audio','clean_audio')