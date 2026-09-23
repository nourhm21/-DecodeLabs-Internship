
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BOT_NAME = "Nova"

# -----------------------------------------------------------------
# 1) KNOWLEDGE BASE  (the "database" of intents -> responses)
#    A dictionary gives O(1) constant-time lookup, unlike a long
#    if/elif ladder which is O(n) and hard to maintain.
# -----------------------------------------------------------------
RESPONSES = {
    "hello": ["Hi there! I'm Nova. How can I help you today?", "Hey! Good to see you."],
    "hi": ["Hello!", "Hi! What's on your mind?"],
    "how are you": ["I'm doing great, thanks for asking!", "Running smoothly, thank you!"],
    "what is your name": ["I'm Nova, your friendly rule-based chatbot."],
    "help": ["I can chat about greetings, my name, or you can just say bye to reset."],
    "who made you": ["I was built as part of the DecodeLabs AI Internship, Project 1."],
    "what can you do": ["Right now I follow fixed rules  no real thinking, just pattern matching!"],
    "thank you": ["You're very welcome!", "Anytime!"],
    "thanks": ["No problem at all!"],
    "bye": ["Goodbye! Have a great day.", "See you later!"],
}

EXIT_WORDS = {"bye", "exit", "quit"}

SUGGESTIONS = [
    "hello", "hi", "how are you", "who made you", "what is your name",
    "what can you do", "help", "thanks", "thank you", "bye",
]

# Punctuation we strip during sanitization
_PUNCT = ".,/#!$%^&*;:{}=-_`~()?'\""


# -----------------------------------------------------------------
# 2) INPUT SANITIZATION
#    lower() + strip() + remove punctuation + collapse whitespace
# -----------------------------------------------------------------
def sanitize(text: str) -> str:
    text = text.lower().strip()
    text = "".join(ch for ch in text if ch not in _PUNCT)
    text = " ".join(text.split())  # collapse multiple spaces
    return text


# -----------------------------------------------------------------
# 3) NESTED / CONDITIONAL LOGIC
#    Demonstrates if/elif decision-making beyond plain dictionary
#    lookup (e.g. "good morning" vs "good night" vs generic "good").
# -----------------------------------------------------------------
def smart_reply(clean_text: str):
    if "good" in clean_text:
        if "morning" in clean_text:
            return "Good morning! Hope you have a productive day."
        elif "night" in clean_text:
            return "Good night! Sleep well."
        else:
            return "Glad to hear that!"
    return None


# -----------------------------------------------------------------
# 4) MAIN DECISION ENGINE (the heart of the rule-based system)
# -----------------------------------------------------------------
def get_reply(raw_text: str) -> str:
    clean = sanitize(raw_text)

    # Exit strategy
    if clean in EXIT_WORDS:
        return random.choice(RESPONSES["bye"])

    # Nested/contextual rules
    nested = smart_reply(clean)
    if nested:
        return nested

    # Dictionary lookup with fallback -> the ".get()" pattern
    reply = RESPONSES.get(clean)
    if reply:
        return random.choice(reply) if isinstance(reply, list) else reply

    return "I don't understand that yet. Could you rephrase?"


# -----------------------------------------------------------------
# ROUTES
# -----------------------------------------------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        bot_name=BOT_NAME,
        suggestions=SUGGESTIONS,
        greeting=f'Hello! I\'m {BOT_NAME}, a rule-based chatbot. '
                  f'Type "bye" to reset, or use a suggestion below.',
    )


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")

    if not user_message.strip():
        return jsonify({"reply": "Please type something."})

    reply = get_reply(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    # "while True" equivalent: the dev server keeps running,
    # continuously accepting new /chat requests until stopped.
    app.run(debug=True, host="0.0.0.0", port=5000)
