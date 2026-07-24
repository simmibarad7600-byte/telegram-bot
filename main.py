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

# Repeated/Duplicate messages ko rokne ke liye memory cache
forwarded_messages_cache = set()

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
        # Message ki unique identity banayein duplicate rokne ke liye
        msg_identifier = text.strip()
        if not msg_identifier:
            msg_identifier = str(message.id)

        # 3. Check karein ki kya yeh message pehle hi forward ho chuka hai
        if msg_identifier in forwarded_messages_cache:
            return  # Agar pehle se bhej diya hai, toh dobara nahi bheja jayega

        try:
            # Target chat mein message forward kar dein
            await message.forward(chat_id=TARGET_CHAT)
            
            # Cache mein save kar lein
            forwarded_messages_cache.add(msg_identifier)
            
            # Memory clean rakhne ke liye cache ka size limit karein
            if len(forwarded_messages_cache) > 2000:
                forwarded_messages_cache.pop()
                
            print(f"✅ Unique Approved message forwarded from chat: {message.chat.id}")
        except Exception as e:
            print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🚀 GLOBAL DEDUPLICATED FORWARDER READY 🚀")
    print("==========================================")
    app.run()
