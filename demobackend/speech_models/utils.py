from speech_models.preprocess import audio_spec, spec_audio, audio_files_to_numpy
from speech_models.model import model_out
import os
from speech_denoise_api.models import AudioFile
from demobackend.settings import BASE_DIR
import subprocess

def denoise_audio(audio_file_object):
    #audio_file_details = AudioFile.objects.create(input_audio = file_path_object)
    audio_file_path = os.path.join(BASE_DIR, "media", audio_file_object.input_audio_wav.name)
    # if audio_file_path.endswith('.mp3'):
    #     subprocess.call(['ffmpeg', '-i', audio_file_path, audio_file_path[:-4] + '.wav'])
    #     audio_file_path = audio_file_path[:-4] + '.wav'
    raw_audio = audio_files_to_numpy([audio_file_path], 8000, 8064, 8064, 1.0)
    amp_spec, phase_spec = audio_spec(raw_audio)
    model_output = model_out(amp_spec)
    print(audio_file_path.split("/")[-1])
    clean_audio_file_path = spec_audio(model_output, phase_spec, audio_file_path.split("/")[-1])
    audio_file_object.clean_audio = clean_audio_file_path
    audio_file_object.save()
    return clean_audio_file_path

def convert_mp3_to_wav(audio_file_object):
    subprocess.call(['ffmpeg', '-i', os.path.join(BASE_DIR, 'media', 
                    audio_file_object.input_audio_other.name),
                    os.path.join(BASE_DIR, 'media', 
                    str(audio_file_object.input_audio_other.name)[:-4] + '.wav')])
    audio_file_object.input_audio_wav = audio_file_object.input_audio_other.name[:-4] + '.wav'
    audio_file_object.save()