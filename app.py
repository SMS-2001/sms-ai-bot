from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    if not API_KEY:
        return jsonify({"reply": "API Key missing!"})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": user_msg}]
        }]
    }

    try:
    response = requests.post(url, json=payload, timeout=10)
    data = response.json()

    reply = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "AI response error 😢")
    )
except:
    reply = "AI not responding 😢"
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
