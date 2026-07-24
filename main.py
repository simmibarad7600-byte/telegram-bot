import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID", "8391628"))
API_HASH = os.getenv("API_HASH", "85d7a5e61b4054a8f29755a6172e45bf")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Jis group mein messages forward karne hain (Target Chat)
TARGET_CHAT = -1001896213793

# Allowed Countries Filter
ALLOWED_COUNTRIES = ["united states", "france", "spain", "italy"]

# Yahan koi SOURCE_CHATS nahi rakha hai, isliye yeh poore Telegram par kaam karega
@app.on_message()
async def forward_messages(client: Client, message: Message):
    text = message.text or message.caption or ""
    text_lower = text.lower()
    
    # 1. Check karein ki message "approved" hai ya nahi
    if "approved" not in text_lower:
        return
    
    # 2. Check karein ki allowed countries mein se koi keyword hai ya nahi
    is_allowed = any(country in text_lower for country in ALLOWED_COUNTRIES)
    
    if is_allowed:
        try:
            # Target chat mein message forward kar dein
            await message.forward(chat_id=TARGET_CHAT)
            print(f"✅ Global Approved & Matched message forwarded from chat: {message.chat.id}")
        except Exception as e:
            print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🚀 GLOBAL APPROVED FORWARDER READY 🚀")
    print("==========================================")
    app.run()
