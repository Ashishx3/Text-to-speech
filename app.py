<<<<<<< HEAD
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
=======
from flask import Flask, request, render_template, send_file
from gtts import gTTS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form.get('text', '').strip()  # Get text input from the form
    if not text:
        return "Error: No text provided!", 400  # Handle empty input gracefully

    try:
        # Generate speech using gTTS
        tts = gTTS(text)
        # Save the file in a writable temporary directory
        file_path = "/tmp/output.mp3"
        tts.save(file_path)
        return render_template('index.html', audio_path="output.mp3")
    except Exception as e:
        # Handle any exceptions during text-to-speech generation
        return f"Error generating speech: {str(e)}", 500

@app.route('/download/<path:filename>')
def download(filename):
    # Serve the generated MP3 file for download
    return send_file(f"/tmp/{filename}", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, jsonify, send_file
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os
import uuid

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API key from .env
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

# Voice IDs
VOICE_IDS = {
    "male": "X0Kc6dUd5Kws5uwEyOnL",  # Male voice ID
    "female": "Sm1seazb4gs7RSlUVw7c"  # Female voice ID
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    try:
        text = request.form.get("text")
        voice_type = request.form.get("voice", "male")  # Default to male if not selected
        voice_id = VOICE_IDS.get(voice_type, VOICE_IDS["male"])  # Get voice ID

        if not text:
            return jsonify({"error": "Text input is required!"}), 400

        # Generate unique filename
        output_folder = "static/output"
        os.makedirs(output_folder, exist_ok=True)
        filename = f"output_audio_{uuid.uuid4().hex}.mp3"
        output_file_path = os.path.join(output_folder, filename)

        # Convert text to speech
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        # Save the audio file
        with open(output_file_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)

        return jsonify({"audio_url": f"/{output_file_path}"})  # Return audio file path

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the generated audio file
@app.route("/static/output/<filename>")
def serve_audio(filename):
    return send_file(f"static/output/{filename}")

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 30d2f26 (Reconnected repo after formatting)
