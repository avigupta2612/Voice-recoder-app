from django.db.models.lookups import EndsWith
from .serializers import AudioFileModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from demobackend.settings import BASE_DIR
from speech_models.utils import convert_mp3_to_wav, denoise_audio
from speech_models.model import s2t_predictions
import json
from .models import AudioFile

class UploadAudioFileViewSet(APIView):
    def post(self, request):
        file_path_object=request.data['uploaded_file']
        if file_path_object.name.endswith(".wav"):
            audio_file_object = AudioFile.objects.create(input_audio_wav = file_path_object)  
        else:
            audio_file_object = AudioFile.objects.create(input_audio_other = file_path_object)
            convert_mp3_to_wav(audio_file_object)
        data = {
            #'userID': file_object.userID,
            #'recordingId': json.loads(request.data['body'])['recordingId'],
            'id': audio_file_object.id,
            'audioUrl': '/media/' + audio_file_object.input_audio_wav.name,
            #'cleanAudio': '/media/' + file_object.clean_audio.name
        }
        print(data)
        return Response(data,status=status.HTTP_201_CREATED)

class DenoiseAudioFileViewSet(APIView):
    def post(self, request):
        audio_id = request.data['id']
        audio_file_object = AudioFile.objects.get(id = audio_id)
        clean_audio_file_path = denoise_audio(audio_file_object=audio_file_object)       
        data = {
            #'userID': file_object.userID,
            #'recordingId': json.loads(request.data['body'])['recordingId'],
            'id': audio_file_object.id,
            'cleanAudioUrl': '/media/' + audio_file_object.clean_audio.name
        }
        print(data)
        return Response(data,status=status.HTTP_201_CREATED)

class Speech2TextView(APIView):
    def post(self, request):
        audio_id = request.data['id']
        audio_file_object = AudioFile.objects.get(id = audio_id)
        predicted_text = s2t_predictions(audio_file_object)
        data = {
            'text': predicted_text
        }
        return Response(data, status=status.HTTP_200_OK)