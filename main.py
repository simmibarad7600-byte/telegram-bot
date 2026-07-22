from pyrogram import Client, filters, idle
from collections import deque
from flask import Flask
import threading
import asyncio

# 1. Render ke liye chhota sa Dummy Web Server
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running 24/7 successfully!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

# Server ko background thread mein chalu kar rahe hain
threading.Thread(target=run_web).daemon = True


# 2. Aapki API Details
API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"

# Pyrogram Client
app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

# 3. Group IDs (Jahan se messages aayenge)
SOURCE_GROUP_IDS = [
    -1001650537937,
    -1003933792726,
    -1004438106656,
    -1001491105566
]

# Aapka Target Group
TARGET_GROUP_ID = -1001896213793

# 4. Filter Keywords (Ukraine, UK, Australia, Brazil hata diye gaye hain)
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

recent_messages = deque(maxlen=100)

@app.on_message(filters.chat(SOURCE_GROUP_IDS))
async def forward_filtered_messages(client, message):
    if message.text:
        text_lower = message.text.lower()
        found = any(kw in text_lower for kw in TARGET_KEYWORDS)
        
        if found:
            if message.text not in recent_messages:
                print(f"[✅] Kaam ka naya message mila! Forward kar raha hoon...")
                try:
                    await client.send_message(TARGET_GROUP_ID, message.text)
                    recent_messages.append(message.text)
                    print(f"[🚀] Message successfully aapke group mein bhej diya gaya!")
                    print("-" * 50)
                except Exception as e:
                    print(f"[❌] Message bhejne mein error: {e}")
                    print("-" * 50)
            else:
                print(f"[⚠️] Yeh message pehle aa chuka hai (Duplicate). Ignore kar diya.")

print("==================================================")
print("       🚀 LIVE FORWARDER USERBOT READY 🚀       ")
print("==================================================")

async def main():
    await app.start()
    await idle()

asyncio.run(main())
