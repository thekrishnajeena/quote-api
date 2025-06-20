from flask import Flask, jsonify, Response
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# 🔸 Root route that returns a beautiful HTML message
@app.route("/", methods=["GET"])
def home():
    html = """
    <html>
        <head>
            <title>Quote API</title>
            <style>
                body {
                    background-color: #f2f2f2;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                    font-family: 'Segoe UI', sans-serif;
                }
                h1 {
                    font-size: 3rem;
                    color: #333;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>This is <span style="color: #4CAF50;">The Quote Fountain</span></h1>
        </body>
    </html>
    """
    return Response(html, mimetype='text/html')

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
