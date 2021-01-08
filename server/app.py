from flask import Flask, request
from flask_cors import CORS
from preprocess import audio_spec, spec_audio, audio_files_to_numpy 
from model import model_out

raw_audio = []

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods = ["GET"])
def send_response():
    return "1"
@app.route("/sendaudio", methods = ["GET"])
def send_audio():
    print(type(raw_audio))
    amp_spec, phase_spec = audio_spec(raw_audio)
    model_output = model_out(amp_spec)
    clean_audio = spec_audio(model_output, phase_spec)
    return clean_audio

@app.route("/recieveaudio", methods = ["GET", "POST"])
def recieve_audio():
    global raw_audio
    if request.method == "POST":
        f = request.files['files']
        raw_audio = audio_files_to_numpy(f, sample_rate = 8000, 
                    frame_length = 8064, hop_length_frame= 8064, min_duration = 1.0)
      
    return type(f)




if __name__ == '__main__':
    app.run()