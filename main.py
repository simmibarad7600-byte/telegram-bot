import os
import traceback
from pyrogram import Client
from flask import Flask
import threading

# 1. Render ke liye Web Server
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. Telegram Configuration
API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"

try:
    app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

    SOURCE_GROUP_IDS = [
        -1001650537937,
        -1003933792726,
        -1004438106656,
        -1001491105566
    ]
    TARGET_GROUP_ID = -1001896213793

    TARGET_KEYWORDS = [
        "united states",
        "france",
        "spain",
        "italy",
        "germany",
        "canada",
        "5",
        "5 series",
        "series 5"
    ]

    @app.on_message()
    async def forward_filtered_messages(client, message):
        try:
            if message.chat and message.chat.id in SOURCE_GROUP_IDS:
                if message.text:
                    text_lower = message.text.lower()
                    if any(kw in text_lower for kw in TARGET_KEYWORDS):
                        await client.send_message(TARGET_GROUP_ID, message.text)
                        print("[🚀] Message forwarded successfully!")
        except Exception as e:
            print(f"[❌] Message Error: {e}")

    print("==================================================")
    print("       🚀 LIVE FORWARDER USERBOT READY 🚀       ")
    print("==================================================")

except Exception as e:
    print("[❌] Startup Crash Error:")
    traceback.print_exc()

if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        print(f"[❌] App Run Error: {e}")
        traceback.print_exc()
