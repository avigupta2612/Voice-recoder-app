# from django.urls import path, include
# from rest_framework import routers
# from . import views

# router = routers.DefaultRouter()
# router.register(r'denoise_audio', views.AudioFileViewSet)
# urlpatterns = [
#     path('', include(router.urls))
# ]
from django.conf.urls import url
from .views import UploadAudioFileViewSet, Speech2TextView, DenoiseAudioFileViewSet, ShowUserRecordingsView

urlpatterns = [
    url('upload_audio', UploadAudioFileViewSet.as_view()),
    url('denoise_audio', DenoiseAudioFileViewSet.as_view()),
    url('convert_s2t', Speech2TextView.as_view()),
    url('user_recordings', ShowUserRecordingsView.as_view())
]
