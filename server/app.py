from flask import Flask, request
from flask_cors import CORS
from preprocess import audio_spec, spec_audio, audio_files_to_numpy 
from model import model_out
from werkzeug.utils import secure_filename

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
        f = open('./file.wav', 'wb')
        f.write(request.get_data("audio_data"))
        f.close()    
        
        
    return raw_audio




if __name__ == '__main__':
    app.run()
