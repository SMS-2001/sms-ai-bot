from flask import Flask, render_template, request, jsonify
import requests
import os
import re
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


def call_gemini(prompt):
    # ✅ STABLE MODEL (IMPORTANT FIX)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, json=payload, timeout=15)
    data = response.json()

    # ❌ ERROR CHECK
    if "error" in data:
        print("API ERROR:", data["error"])
        return None

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        print("BAD RESPONSE:", data)
        return None


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    if not user_msg:
        return jsonify({"reply": "No message received 😢"})

    if not API_KEY:
        return jsonify({"reply": "API Key missing 😢"})

    # 🧠 Prompt
    prompt = "Answer in simple Hindi for students:\n" + user_msg

    # 🔥 CALL AI
    reply = call_gemini(prompt)

    # 🔁 SAFE FALLBACK
    if not reply:
        reply = "AI temporarily unavailable 😢 (Check API key / model access)"

    return jsonify({"reply": reply})


# local testing only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
