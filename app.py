from flask import Flask, render_template, request, jsonify
import os
import re
import requests

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


# 🧠 SMART DECISION ENGINE
def choose_model(user_msg: str):
    msg = user_msg.lower()

    # 🧮 Math → fastest model
    if re.fullmatch(r"[0-9\+\-\*\/\s\(\)]+", user_msg):
        return "math"

    # 🧬 Science / Biology / tough topics → pro model
    if any(w in msg for w in ["physics", "chemistry", "biology", "dna", "cell", "theory", "explain deeply"]):
        return "gemini-1.5-pro"

    # 📖 long reasoning / history
    if any(w in msg for w in ["history", "war", "freedom", "independence", "mughal", "british"]):
        return "gemini-1.5-pro"

    # ⚡ normal chat → fast model
    return "gemini-1.5-flash"


# 🚀 CALL GEMINI API

def call_gemini(model, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, json=payload, timeout=15)

    print("MODEL:", model)
    print("RESPONSE:", response.text)   # 🔥 IMPORTANT DEBUG

    return response.json()


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    if not user_msg:
        return jsonify({"reply": "No message received 😢"})

    if not API_KEY:
        return jsonify({"reply": "API Key missing 😢"})

    # 🧮 MATH MODE (instant)
    if re.fullmatch(r"[0-9\+\-\*\/\s\(\)]+", user_msg):
        try:
            return jsonify({"reply": f"🧮 Answer: {eval(user_msg)}"})
        except:
            return jsonify({"reply": "Invalid math expression 😢"})

    # 🧠 MODEL SELECT
    model = choose_model(user_msg)

    prompt = "Answer in simple Hindi for students:\n" + user_msg

    reply = None

    # 🔥 PRIMARY TRY
    try:
        data = call_gemini(model, prompt)

        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        reply = None

    # 🔁 FALLBACK SYSTEM
    if not reply:
        fallback_models = ["gemini-1.5-flash", "gemini-pro"]

        for m in fallback_models:
            try:
                data = call_gemini(m, prompt)

                if "candidates" in data:
                    reply = data["candidates"][0]["content"]["parts"][0]["text"]
                    break
            except:
                continue

    if not reply:
        reply = "AI temporarily unavailable 😢"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
