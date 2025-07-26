from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
import os
import uuid
import glob

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cleanup_old_files():
    """Delete old voice files from the static folder."""
    old_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "voice_*.mp3"))
    for file in old_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    gender = request.form['gender']

    cleanup_old_files()

    unique_filename = f"voice_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        lang = 'hi'
        tts = gTTS(text=text, lang=lang, slow=False, tld='com' if gender == 'male' else 'co.in')
        tts.save(audio_path)
    except Exception as e:
        return render_template('index.html', error="Error generating audio. Please try again!")

    return render_template('index.html', audio_path=unique_filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Ensure app is callable:
# Vercel automatically detects and serves `app`.
