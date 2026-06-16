from flask import Flask, render_template, request, jsonify
import requests
import os
import re

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    if not user_msg:
        return jsonify({"reply": "No message received 😢"})

    if not API_KEY:
        return jsonify({"reply": "API Key missing 😢"})

    msg_lower = user_msg.lower()

    # 🧮 MATH MODE
    if re.fullmatch(r"[0-9\+\-\*\/\s\(\)]+", user_msg):
        try:
            result = eval(user_msg)
            return jsonify({"reply": f"🧮 Answer: {result}"})
        except:
            return jsonify({"reply": "Invalid math expression 😢"})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    # 🧠 BIOLOGY MODE
    if any(word in msg_lower for word in ["biology", "cell", "dna", "plant", "human", "body", "heart", "blood"]):
        prompt = "You are a biology teacher. Explain in simple Hindi + English:\n" + user_msg

    # 📜 HISTORY MODE
    elif any(word in msg_lower for word in ["history", "war", "independence", "freedom", "king", "mughal", "british"]):
        prompt = "You are a history teacher. Explain in simple Hindi + English:\n" + user_msg

    # 🤖 GENERAL MODE
    else:
        prompt = "Answer in simple clear way for students:\n" + user_msg

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        reply = None

        if "candidates" in data and len(data["candidates"]) > 0:
            content = data["candidates"][0].get("content", {})
            parts = content.get("parts", [])

            if len(parts) > 0:
                reply = parts[0].get("text")

        if not reply:
            reply = "AI response empty 😢"

    except Exception:
        reply = "AI not responding 😢"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
