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
    msg_lower = user_msg.lower()

    if not user_msg:
        return jsonify({"reply": "No message received 😢"})

    if not API_KEY:
        return jsonify({"reply": "API Key missing 😢"})

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
        payload = {
            "contents": [{
                "parts": [{
                    "text": "You are a biology teacher. Explain in simple Hindi + English:\n" + user_msg
                }]
            }]
        }

    # 📜 HISTORY MODE
    elif any(word in msg_lower for word in ["history", "war", "independence", "freedom", "king", "mughal", "british"]):
        payload = {
            "contents": [{
                "parts": [{
                    "text": "You are a history teacher. Explain in simple Hindi + English:\n" + user_msg
                }]
            }]
        }

    # 🤖 GENERAL MODE
    else:
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Answer in simple and clear way for students:\n" + user_msg
                }]
            }]
        }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        reply = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text")
        )

        if not reply:
            reply = "AI response empty 😢"

    except:
        reply = "AI not responding 😢"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
