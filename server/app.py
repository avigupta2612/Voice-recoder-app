from flask import Flask, request, redirect, send_from_directory, jsonify
from flask_cors import CORS
from preprocess import audio_spec, spec_audio, audio_files_to_numpy
from model import model_out
from werkzeug.utils import secure_filename
import os


UPLOAD_DIRECTORY = "../localDB/uploadedAudio"
DOWNLOAD_DIRECTORY = "../localDB/cleanAudio"

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=["GET"])
def send_response():
    return "1"


''' @app.route("/get_clean_audio", methods = ["GET"])
def send_audio():
    raw_audio = audio_files_to_numpy(['./localDB/uploadedAudio/file.wav'], 8000, 8064, 8064, 1.0)
    amp_spec, phase_spec = audio_spec(raw_audio)
    model_output = model_out(amp_spec)
    clean_audio = spec_audio(model_output, phase_spec)
    return clean_audio
'''


@app.route("/upload_audio", methods=["GET", "POST"])
def recieve_audio():
    if request.method == "POST":
        f = request.files['audio_data']
        with open(os.path.join(UPLOAD_DIRECTORY, f.filename), 'wb') as audio:
            f.save(audio)
        raw_audio = audio_files_to_numpy(
            [os.path.join(UPLOAD_DIRECTORY, f.filename)], 8000, 8064, 8064, 1.0)
        amp_spec, phase_spec = audio_spec(raw_audio)
        model_output = model_out(amp_spec)
        clean_audio = spec_audio(model_output, phase_spec, f.filename)
        #return send_from_directory(DOWNLOAD_DIRECTORY, clean_audio, as_attachment=True)
        return jsonify(url=os.path.join(DOWNLOAD_DIRECTORY+'/'+clean_audio))

if __name__ == '__main__':
    app.run()
