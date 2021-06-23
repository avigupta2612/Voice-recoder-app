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
        try:
            email_id = request.data['email_id']
            if file_path_object.name.endswith(".wav"):
                audio_file_object = AudioFile.objects.create(input_audio_wav = file_path_object, 
                                                            userId = email_id)
                data = {
                    'id': audio_file_object.id,
                    'audioUrl': '/media/' + audio_file_object.input_audio_wav.name,
                    'userId': audio_file_object.userId
                }  
            else:
                audio_file_object = AudioFile.objects.create(input_audio_other = file_path_object,
                                                            userId = email_id)
                convert_mp3_to_wav(audio_file_object)
                data = {
                    'id': audio_file_object.id,
                    'audioUrl': '/media/' + audio_file_object.input_audio_wav.name,
                    'userId': audio_file_object.userId
                }
        except:
            if file_path_object.name.endswith(".wav"):
                audio_file_object = AudioFile.objects.create(input_audio_wav = file_path_object)
                data = {
                    'id': audio_file_object.id,
                    'audioUrl': '/media/' + audio_file_object.input_audio_wav.name,
                } 
            else:
                audio_file_object = AudioFile.objects.create(input_audio_other = file_path_object)
                convert_mp3_to_wav(audio_file_object)
                data = {
                    'id': audio_file_object.id,
                    'audioUrl': '/media/' + audio_file_object.input_audio_wav.name,
                }
        return Response(data,status=status.HTTP_201_CREATED)

class DenoiseAudioFileViewSet(APIView):
    def post(self, request):
        audio_id = request.data['id']
        audio_file_object = AudioFile.objects.get(id = audio_id)
        clean_audio_file_path = denoise_audio(audio_file_object=audio_file_object)       
        data = {
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

class ShowUserRecordingsView(APIView):
    def post(self, request):
        email_id = request.data['email_id']
        audio_file_object = AudioFile.objects.filter(userId = email_id)
        data = []
        for i, obj in enumerate(audio_file_object):
            data.append({
                "id" : obj.id,
                "originalAudio" : '/media/' + obj.input_audio_wav.name,
            })
            if obj.clean_audio:
                data[i]["cleanAudio"] = '/media/' + obj.clean_audio.name
        
        return Response(data, status=status.HTTP_200_OK)