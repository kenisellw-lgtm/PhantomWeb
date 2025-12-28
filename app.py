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
        # Check for Server-Side API Key
        api_token = os.getenv("REPLICATE_API_TOKEN")
        if not api_token:
            print("❌ Error: REPLICATE_API_TOKEN is missing from Render settings.")
            return jsonify({"error": "Server Configuration Error: API Key missing"}), 500

        # Get data from frontend
        prompt = request.form.get('prompt')
        file = request.files.get('audio')
        
        if not prompt or not file:
            return jsonify({"error": "Please provide both a prompt and an audio file"}), 400

        print(f"🎵 Starting Remix Job for: {prompt}")

        # Send to Replicate (MusicGen Remix)
        output = replicate.run(
            "meta/musicgen-remix:2541baf69a23f87a885d576a029b360b73c24d101d244670081e74f0775d733e",
            input={
                "input_audio": file,
                "prompt": prompt,
                "duration": 30,
                "model_version": "stereo-large"
            }
        )
        
        print(f"✅ Success! URL: {output}")
        return jsonify({"success": True, "audio_url": output})

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    