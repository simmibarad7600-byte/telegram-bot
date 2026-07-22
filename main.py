import os
import asyncio
from flask import Flask
import threading
import time
import urllib.request
from telethon import TelegramClient, events

# 1. Web Server for Render
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Telethon Bot is active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. Self-Ping mechanism
def self_ping():
    url = "https://telegram-bot-ps39.onrender.com"
    while True:
        try:
            time.sleep(120)
            urllib.request.urlopen(url)
        except Exception:
            pass

threading.Thread(target=self_ping, daemon=True).start()

# 3. Telethon Userbot Configuration
API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"
SESSION_STRING = os.environ.get("SESSION_STRING")

if SESSION_STRING:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
else:
    client = TelegramClient("my_userbot", API_ID, API_HASH)

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
    "germany"
]

@client.on(events.NewMessage(chats=SOURCE_GROUP_IDS))
async def forward_filtered_messages(event):
    try:
        message_text = event.raw_text
        if message_text:
            text_lower = message_text.lower()
            
            # Rule: Ignore if starts with '4' or contains '4 series'
            if text_lower.startswith("4") or "4 series" in text_lower or text_lower.startswith("4 "):
                return
            
            # Rule: Forward only if target keywords match
            if any(kw in text_lower for kw in TARGET_KEYWORDS):
                await client.send_message(TARGET_GROUP_ID, message_text)
                print("[🚀] Message forwarded successfully via Telethon!")
    except Exception as e:
        print(f"[❌ Error]: {e}")

print("==================================================")
print("     🚀 TELETHON LIVE FORWARDER BOT READY 🚀     ")
print("==================================================")

if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
