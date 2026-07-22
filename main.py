import asyncio
import os
from pyrogram import Client
from flask import Flask
import threading
import time
import urllib.request
import re

# Python 3.14 event loop fix
try:
    asyncio.get_running_loop()
except RuntimeError:
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# 1. Render ke liye Web Server
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. Self-Ping mechanism taaki Render sleep na ho
def self_ping():
    url = "https://telegram-bot-ps39.onrender.com"
    while True:
        try:
            time.sleep(120)  # har 2 minute mein ping karega
            urllib.request.urlopen(url)
            print("[Self-Ping] Server pinged successfully!")
        except Exception as e:
            print(f"[Self-Ping Error]: {e}")

threading.Thread(target=self_ping, daemon=True).start()

# 3. Telegram Userbot Configuration
API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"

SESSION_STRING = os.environ.get("SESSION_STRING")

if SESSION_STRING:
    app = Client(
        "my_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )
else:
    app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

SOURCE_GROUP_IDS = [
    -1001650537937,
    -1003933792726,
    -1004438106656,
    -1001491105566
]
TARGET_GROUP_ID = -1001896213793

# Sirf abhi yeh countries / keywords allow honge
TARGET_KEYWORDS = [
    "united states",
    "france",
    "spain",
    "italy",
    "germany"
]

@app.on_message()
async def forward_filtered_messages(client, message):
    try:
        if message.chat and message.chat.id in SOURCE_GROUP_IDS:
            if message.text:
                text_clean = message.text.strip()
                text_lower = text_clean.lower()
                
                # Rule 1: Agar message '4' ya '4 series' se shuru hota hai, toh seedha ignore karo
                if text_lower.startswith("4") or "4 series" in text_lower or re.match(r'^4\b', text_lower):
                    return
                
                # Rule 2: Sirf defined target keywords match hone par hi forward ho
                if any(kw in text_lower for kw in TARGET_KEYWORDS):
                    await client.send_message(TARGET_GROUP_ID, message.text)
                    print("[🚀] Message forwarded successfully!")
    except Exception as e:
        print(f"[❌] Error: {e}")

print("==================================================")
print("       🚀 LIVE FORWARDER USERBOT READY 🚀       ")
print("==================================================")

if __name__ == "__main__":
    app.run()
