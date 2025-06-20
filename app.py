from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route("/")
def home():
    return "<h1>The Quote Fountain is Alive!</h1>"

@app.route("/quote", methods=["GET"])
def get_quote():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY is missing"}), 500

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Give me a unique and thought-provoking quote for today."}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        quote = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"quote": quote})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
