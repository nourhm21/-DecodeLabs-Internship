"""
Nova - Rule-Based AI Chatbot (Project 1 - DecodeLabs Internship)
-----------------------------------------------------------------
PURE PYTHON / TERMINAL VERSION
This file matches the exact specification from the training slides:
  - INPUT LOOP      : a real  while True  loop
  - SANITIZATION    : lower() + strip() + remove punctuation
  - KNOWLEDGE BASE  : dictionary with 5+ intents
  - FALLBACK        : responses.get(key, default)
  - EXIT STRATEGY   : "bye" / "exit" / "quit"  ->  break

"""


import random

BOT_NAME = "Nova"

# -----------------------------------------------------------------
# KNOWLEDGE BASE (dictionary -> O(1) lookup instead of if/elif ladder)
# -----------------------------------------------------------------
responses = {
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

EXIT_WORDS = ("bye", "exit", "quit")
_PUNCT = ".,/#!$%^&*;:{}=-_`~()?'\""


def sanitize(text: str) -> str:
    """Lowercase, strip, remove punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = "".join(ch for ch in text if ch not in _PUNCT)
    text = " ".join(text.split())
    return text


def smart_reply(clean_text: str):
    """Nested/conditional logic beyond plain dictionary lookup."""
    if "good" in clean_text:
        if "morning" in clean_text:
            return "Good morning! Hope you have a productive day."
        elif "night" in clean_text:
            return "Good night! Sleep well."
        else:
            return "Glad to hear that!"
    return None


def get_reply(raw_text: str) -> str:
    clean = sanitize(raw_text)

    nested = smart_reply(clean)
    if nested:
        return nested

    # .get() pattern: lookup + fallback in a single atomic operation
    reply = responses.get(clean, "I don't understand that yet. Could you rephrase?")
    return random.choice(reply) if isinstance(reply, list) else reply


def main():
    print(f"Hello! I'm {BOT_NAME}, a rule-based chatbot. Type 'bye' to exit.\n")

    # ---------------------------------------------------------
    # THE HEARTBEAT: THE INFINITE LOOP
    # The organism stays alive until the Kill Command.
    # ---------------------------------------------------------
    while True:
        user_input = input("You: ")
        clean_input = sanitize(user_input)

        if clean_input in EXIT_WORDS:
            print(f"{BOT_NAME}: {random.choice(responses['bye'])}")
            break  # <-- Kill Command: exits the infinite loop cleanly

        reply = get_reply(user_input)
        print(f"{BOT_NAME}: {reply}")


if __name__ == "__main__":
    main()
