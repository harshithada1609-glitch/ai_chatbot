from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("GROQ_API_KEY"))   # check if API key loads

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Store user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI Interview Assistant."
                },
                *conversation_history
            ]
        )

        bot_reply = response.choices[0].message.content

        # Store assistant reply
        conversation_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)