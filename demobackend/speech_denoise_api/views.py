from .serializers import AudioFileModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from demobackend.settings import BASE_DIR
from speech_models.utils import denoise_audio
from .models import AudioFile


class AudioFileViewSet(APIView):
    def post(self, request):
        file_path_object=request.data['uploaded_file']
        clean_audio_file_path = denoise_audio(file_path_object=file_path_object)
        data = AudioFile.objects.last()
        return Response(data,status=status.HTTP_201_CREATED)