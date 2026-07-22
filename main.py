import sys
import asyncio

# Python 3.14 event loop crash fix
try:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        raise RuntimeError
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import os
from pyrogram import Client
from flask import Flask
import threading
import time
import urllib.request

# 1. Web Server for Hosting
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. Self-Ping mechanism to keep server alive
def self_ping():
    url = "https://telegram-bot-ps39.onrender.com"
    while True:
        try:
            time.sleep(120)
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
    -1003933792726, # Yeh group list mein rahega
    -1004438106656,
    -1001491105566,
    -1003601805762
]
TARGET_GROUP_ID = -1001896213793

TARGET_KEYWORDS = [
    "united states",
    "france",
    "spain",
    "italy",
    "germany",
    "test message"
]

# Safely cache peers without crashing if any group fails or restricts access
async def cache_peers():
    try:
        await app.start()
        print("[i] Attempting to cache chat peers...")
        for chat_id in SOURCE_GROUP_IDS:
            try:
                await app.get_chat(chat_id)
                print(f"[✓] Cached source chat: {chat_id}")
            except Exception as e:
                print(f"[!] Skipped/Ignored chat {chat_id} due to restriction: {e}")
        try:
            await app.get_chat(TARGET_GROUP_ID)
            print(f"[✓] Cached target chat: {TARGET_GROUP_ID}")
        except Exception as e:
            print(f"[!] Could not cache target {TARGET_GROUP_ID}: {e}")
        await app.stop()
    except Exception as e:
        print(f"[!] Cache warning: {e}")

@app.on_message()
async def forward_country_messages(client, message):
    try:
        if message.chat:
            chat_id = message.chat.id
            if chat_id in SOURCE_GROUP_IDS:
                if message.text:
                    text_clean = message.text.strip()
                    text_lower = text_clean.lower()
                    
                    if any(kw in text_lower for kw in TARGET_KEYWORDS):
                        await client.send_message(TARGET_GROUP_ID, message.text)
                        print("[🚀] Filter matched & message forwarded successfully!")
    except Exception as e:
        pass

print("==================================================")
print("        🚀 LIVE FORWARDER USERBOT READY 🚀        ")
print("==================================================")

if __name__ == "__main__":
    try:
        loop.run_until_complete(cache_peers())
    except Exception:
        pass
    app.run()
