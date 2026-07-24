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

# Track karne ke liye dictionary
sent_transactions = {}
TIME_WINDOW = 900  # 15 minutes

def extract_unique_identifier(text: str) -> str:
    # Message ke andar se card number, amount, ya specific unique numbers/words nikalne ki koshish karenge
    # Isse agar wahi transaction doosre text ke sath aayegi toh bhi pakdi jayegi
    text_lower = text.lower()
    
    # Agar text mein koi numbers (jaise card ke digits ya amounts) hain, unhe extract karo
    numbers = "".join(re.findall(r'\d+', text_lower))
    
    # Agar numbers milte hain toh unka use karenge, warna core text ka
    if len(numbers) > 4:
        return numbers[-10:] # Last 10 digits unique tracking ke liye
    
    return re.sub(r'[^a-zA-Z0-9]', '', text_lower)

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
        identifier = extract_unique_identifier(text)
        
        if not identifier or len(identifier) < 4:
            return

        # Purane entries saaf karein
        expired_keys = [k for k, timestamp in sent_transactions.items() if current_time - timestamp > TIME_WINDOW]
        for k in expired_keys:
            del sent_transactions[k]

        # Check karein ki kya yeh transaction/message pehle aa chuka hai
        if identifier in sent_transactions:
            print(f"⏩ Ek hi transaction ka doosra message rok liya gaya!")
            return

        try:
            await message.forward(chat_id=TARGET_CHAT)
            
            # Save karein
            sent_transactions[identifier] = current_time
                
            print(f"✅ Pehla approved message successfully forward kiya gaya!")
        except Exception as e:
            print(f"Error forwarding message: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("🚀 SMART TRANSACTION DEDUPLICATOR READY 🚀")
    print("==========================================")
    app.run()
