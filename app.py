from flask import Flask, render_template, request, jsonify
import os
import re
import requests

app = Flask(__name__)

# 🔑 Render Environment Variable
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
            return jsonify({"reply": f"🧮 Answer: {eval(user_msg)}"})
        except:
            return jsonify({"reply": "Invalid math expression 😢"})

    # 🧠 PROMPT ENGINE
    if any(w in msg_lower for w in ["biology", "cell", "dna", "heart", "blood", "plant"]):
        prompt = "You are a biology teacher. Explain in simple Hindi:\n" + user_msg

    elif any(w in msg_lower for w in ["history", "war", "independence", "freedom", "king"]):
        prompt = "You are a history teacher. Explain in simple Hindi:\n" + user_msg

    elif "story" in msg_lower:
        prompt = "Write a simple interesting story in Hindi:\n" + user_msg

    else:
        prompt = "Answer in simple Hindi for students:\n" + user_msg

    # 🤖 GEMINI API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()

        # ❗ ERROR CHECK
        if "error" in data:
            return jsonify({"reply": "API Error: " + data["error"]["message"]})

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
