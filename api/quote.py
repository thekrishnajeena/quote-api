from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route("/api/quote", methods=["GET"])
def get_quote():
    if not GEMINI_API_KEY:
        return jsonify({"error": "API key missing"}), 500

    payload = {
        "contents": [{
            "parts": [{
                "text": "Give me a unique and thought-provoking quote for today..."
            }]
        }]
    }

    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        data = response.json()
        quote = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"quote": quote})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel
def handler(environ, start_response):
    return app(environ, start_response)
