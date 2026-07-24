import os
import re
import time
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

TARGET_CHAT = -1001896213793
ALLOWED_COUNTRIES = ["united states", "france", "spain", "italy"]

# Message text aur uska bhejne ka time store karne ke liye dictionary
recent_messages = {}
# Duplicate rokne ka time window (Jaise: 10 minutes tak same message dobara nahi aana chahiye)
TIME_WINDOW = 600  # seconds (10 minutes)

def get_core_text(text: str) -> str:
    # Numbers, symbols aur extra spaces hata kar sirf main words rakhenge
    clean = re.sub(r'[^a-zA-Z]', '', text.lower())
    return clean

@app.on_message()
async def forward_messages(client: Client, message: Message):
    text = message.text or message.caption or ""
    text_lower = text.lower()
    
    # 1. Approved check
    if "approved" not in text_lower:
        return
    
    # 2. Country check
    is_allowed = any(country in text_lower for country in ALLOWED_COUNTRIES)
    
    if is_allowed:
        current_time = time.time()
        core_text = get_core_text(text)
        
        if not core_text:
            return

        # Purane entries saaf karein jo time window se bahar ho gaye hain
        expired_keys = [k for k, timestamp in recent_messages.items() if current_time - timestamp > TIME_WINDOW]
        for k in expired_keys:
            del recent_messages[k]

        # Check karein ki kya yeh core text pichle 10 minutes mein already bheja gaya hai
        is_duplicate = False
        for sent_text in recent_messages.keys():
            # Agar text ka 80% hissa match hota hai toh duplicate maan lo
            if core_text == sent_text or (len(core_text) > 20 and (core_text in sent_text or sent_text in core_text)):
                is_duplicate = True
                break

        if is_duplicate:
            print(f"⏩ Time-window duplicate message pakda gaya aur skip kiya gaya!")
            return

        try:
            await message.forward(chat_id=TARGET_CHAT)
            
            # Current message ko time ke sath store kar lein
            recent_messages[core_text] = current_time
                
            print(f"✅ Fresh Approved message successfully forwarded!")
        except Exception as e:
            print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🚀 TIME-BASED SMART DEDUPLICATION READY 🚀")
    print("==========================================")
    app.run()
