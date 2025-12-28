import os
from flask import Flask, render_template, request, jsonify
import replicate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- ROUTE 1: Serve the Website ---
@app.route('/')
def home():
    return render_template('index.html')

# --- ROUTE 2: Handle the Remix (Secure Backend) ---
@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 1. Check for API Key
        api_token = os.getenv("REPLICATE_API_TOKEN")
        if not api_token:
            print("❌ Error: REPLICATE_API_TOKEN is missing.")
            return jsonify({"error": "Server Error: API Key missing"}), 500

        # 2. Get data from frontend
        prompt = request.form.get('prompt')
        file = request.files.get('audio')
        
        if not prompt or not file:
            return jsonify({"error": "Missing prompt or audio file"}), 400

        print(f"🎵 Received file: {file.filename}")
        print(f"🎵 Prompt: {prompt}")

        # 3. Save file temporarily
        temp_filename = "temp_upload.wav"
        file.save(temp_filename)
        input_file = open(temp_filename, "rb")

        # 4. Send to Replicate (UPDATED MODEL ID)
        print("📡 Sending to Replicate...")
        
        output = replicate.run(
            # This is the Official Meta MusicGen (Melody/Stereo) Version
            "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
            input={
                "input_audio": input_file,
                "prompt": prompt,
                "duration": 30,
                "model_version": "stereo-melody-large", # Crucial for Remixing!
                "normalization_strategy": "peak"
            }
        )
        
        print(f"✅ Success! URL: {output}")
        return jsonify({"success": True, "audio_url": output})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500