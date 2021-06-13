# from django.urls import path, include
# from rest_framework import routers
# from . import views

# router = routers.DefaultRouter()
# router.register(r'denoise_audio', views.AudioFileViewSet)
# urlpatterns = [
#     path('', include(router.urls))
# ]
from django.conf.urls import url
from .views import AudioFileViewSet

urlpatterns = [
    url('denoise_audio', AudioFileViewSet.as_view()),
]
