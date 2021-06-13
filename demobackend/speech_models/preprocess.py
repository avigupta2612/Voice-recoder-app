import numpy as np
import os
import librosa
import soundfile as sf
from demobackend.settings import MEDIA_ROOT

def audio_to_audio_frame_stack(sound_data, frame_length, hop_length_frame):
    """This function take an audio and split into several frame
       in a numpy matrix of size (nb_frame,frame_length)"""

    sequence_sample_length = sound_data.shape[0]

    sound_data_list = [sound_data[start:start + frame_length] for start in range(
    0, sequence_sample_length - frame_length + 1, hop_length_frame)]  # get sliding windows
    try:
        sound_data_array = np.vstack(sound_data_list)
        return sound_data_array
    except ValueError:
        pass

def audio_files_to_numpy(list_audio_files, sample_rate, frame_length, hop_length_frame, min_duration):
    """This function take audio files of a directory and merge them
    in a numpy matrix of size (nb_frame,frame_length) for a sliding window of size hop_length_frame"""

    list_sound_array = []

    for file in list_audio_files:
        # open the audio file
        y, sr = librosa.load(file, sr=sample_rate)
        total_duration = librosa.get_duration(y=y, sr=sr)

        if (total_duration >= min_duration):
            list_sound_array.append(audio_to_audio_frame_stack(
                y, frame_length, hop_length_frame))
    #print(list_sound_array)    
    return np.vstack(list_sound_array)

def audio_to_magnitude_db_and_phase(n_fft, hop_length_fft, audio):
    """This function takes an audio and convert into spectrogram,
       it returns the magnitude in dB and the phase"""

    stftaudio = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length_fft)
    stftaudio_magnitude, stftaudio_phase = librosa.magphase(stftaudio)

    stftaudio_magnitude_db = librosa.amplitude_to_db(
        stftaudio_magnitude, ref=np.max)

    return stftaudio_magnitude_db, stftaudio_phase


def numpy_audio_to_matrix_spectrogram(numpy_audio, dim_square_spec, n_fft, hop_length_fft):
    """This function takes as input a numpy audi of size (nb_frame,frame_length), and return
    a numpy containing the matrix spectrogram for amplitude in dB and phase. It will have the size
    (nb_frame,dim_square_spec,dim_square_spec)"""

    nb_audio = numpy_audio.shape[0]

    m_mag_db = np.zeros((nb_audio, dim_square_spec, dim_square_spec))
    m_phase = np.zeros((nb_audio, dim_square_spec, dim_square_spec), dtype=complex)

    for i in range(nb_audio):
        m_mag_db[i, :, :], m_phase[i, :, :] = audio_to_magnitude_db_and_phase(
            n_fft, hop_length_fft, numpy_audio[i])

    return m_mag_db, m_phase


def magnitude_db_and_phase_to_audio(frame_length, hop_length_fft, stftaudio_magnitude_db, stftaudio_phase):
    """This functions reverts a spectrogram to an audio"""

    stftaudio_magnitude_rev = librosa.db_to_amplitude(stftaudio_magnitude_db, ref=1.0)

    # taking magnitude and phase of audio
    audio_reverse_stft = stftaudio_magnitude_rev * stftaudio_phase
    audio_reconstruct = librosa.core.istft(audio_reverse_stft, hop_length=hop_length_fft, length=frame_length)

    return audio_reconstruct

def matrix_spectrogram_to_numpy_audio(m_mag_db, m_phase, frame_length, hop_length_fft)  :
    """This functions reverts the matrix spectrograms to numpy audio"""

    list_audio = []

    nb_spec = m_mag_db.shape[0]

    for i in range(nb_spec):

        audio_reconstruct = magnitude_db_and_phase_to_audio(frame_length, hop_length_fft, m_mag_db[i], m_phase[i])
        list_audio.append(audio_reconstruct)

    return np.vstack(list_audio)

def audio_spec(audio_array):
    #print(audio_array)
    m_amp_db_voice,  m_pha_voice = numpy_audio_to_matrix_spectrogram(
                                    audio_array, dim_square_spec = int(255 / 2) + 1, n_fft = 255, 
                                    hop_length_fft = 63)
    m_amp_db_voice = m_amp_db_voice.reshape(m_amp_db_voice.shape[0],1,128,128)
    m_amp_db_voice = (m_amp_db_voice + 46) / 50

    return m_amp_db_voice, m_pha_voice

def s2t_audio_to_array(path):
    speech, sr = librosa.load(path, sr= 16000)
    return speech

def spec_audio(spec_img, spec_phase, filename):
    spec_img = 50 * spec_img - 46
    numpy_audio = matrix_spectrogram_to_numpy_audio(spec_img, spec_phase, 
                                                    frame_length = 8064, hop_length_fft = 63)
    array_output = numpy_audio.reshape(1,numpy_audio.shape[0]*8064) * 10
    sf.write(os.path.join(MEDIA_ROOT,'clean-audio',filename), array_output[0,:], 8000)                                
    return os.path.join('clean-audio',filename)

 

