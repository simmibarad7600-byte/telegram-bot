import os
import re
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

# Smart duplicate tracking ke liye set
forwarded_signatures = set()

def get_clean_signature(text: str) -> str:
    # Sirf letters aur numbers rakhega, baaki spaces/symbols hata dega taaki match pakka ho sake
    clean_text = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    return clean_text

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
        # Clean signature banayein duplicate rokne ke liye
        signature = get_clean_signature(text)
        
        if not signature:
            signature = str(message.id)

        # 3. Duplicate check
        if signature in forwarded_signatures:
            print(f"⏩ Repeat message pakda gaya aur skip kiya gaya!")
            return

        try:
            await message.forward(chat_id=TARGET_CHAT)
            
            # Signature save karein
            forwarded_signatures.add(signature)
            
            if len(forwarded_signatures) > 3000:
                forwarded_signatures.pop()
                
            print(f"✅ Unique Approved message successfully forwarded!")
        except Exception as e:
            print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🚀 SMART DEDUPLICATED FORWARDER READY 🚀")
    print("==========================================")
    app.run()
