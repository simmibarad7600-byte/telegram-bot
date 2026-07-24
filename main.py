import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Railway / Environment variables se credentials uthayega
API_ID = int(os.getenv("API_ID", "8391628"))
API_HASH = os.getenv("API_HASH", "85d7a5e61b4054a8f29755a6172e45bf")
SESSION_STRING = os.getenv("SESSION_STRING")

# Userbot Client initialize karein
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Jin groups se messages uthane hain (Source Chats - Purana 6020 wala group hata diya hai)
SOURCE_CHATS = [-1001650537937, -1004438106656, -1003933792726]

# Jis group mein messages forward karne hain (Target Chat)
TARGET_CHAT = -1001896213793

# Allowed Countries Filter (Strict check)
ALLOWED_COUNTRIES = ["united states", "france", "spain", "italy"]

@app.on_message(filters.chat(SOURCE_CHATS))
async def forward_messages(client: Client, message: Message):
    text = message.text or message.caption or ""
    text_lower = text.lower()
    
    # 1. Sabse pehle check karein ki message "approved" hai ya nahi (Fake data hatane ke liye)
    if "approved" not in text_lower:
        return  # Agar approved nahi hai, toh yahin rok do
    
    # 2. Check karein ki message mein allowed countries mein se koi keyword hai ya nahi
    is_allowed = any(country in text_lower for country in ALLOWED_COUNTRIES)
    
    if is_allowed:
        try:
            # Target chat mein message forward kar dein
            await message.forward(chat_id=TARGET_CHAT)
            print(f"✅ Approved & Matched message successfully forwarded from {message.chat.id}")
        except Exception as e:
            print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🚀 LIVE FORWARDER USERBOT READY 🚀")
    print("==========================================")
    app.run()
