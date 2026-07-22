from pyrogram import Client, filters
from collections import deque
from flask import Flask
import threading

# 1. Render ka Port requirement poora karne ke liye chhota sa Web Server
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Telegram Userbot is running 24/7!"

def run_web():
    # Render port 10000 expect karta hai web service ke liye
    app_web.run(host="0.0.0.0", port=10000)

# Web server ko background thread mein daal diya taaki bot ko disturb na kare
threading.Thread(target=run_web).daemon = True


# 2. Aapki Telegram API Details
API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"

# Pyrogram Client
app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

# 3. Source Group IDs (Jahan se messages aayenge)
SOURCE_GROUP_IDS = [
    -1001650537937,
    -1003933792726,
    -1004438106656,
    -1001491105566
]

# Aapka Target Group ID
TARGET_GROUP_ID = -1001896213793

# 4. Filter Keywords
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

# Seedha app.run() chala rahe hain taaki background thread ke sath conflict na ho
app.run()
