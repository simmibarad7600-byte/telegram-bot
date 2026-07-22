import os
from pyrogram import Client, filters

# Environment variables se credentials uthana (Railway variables se connect ho jayega)
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Agar aapne source groups aur target group IDs env me rakhe hain ya yahan direct define karne hain
# Yahan apne Source Group IDs aur Target Group ID daal dein
SOURCE_GROUP_IDS = [-1001234567890]  # Yahan apne source groups ki IDs dalein (integer format me)
TARGET_GROUP_ID = -1009876543210    # Yahan apne target group ki ID dalein

# Jin keywords ke aane par message forward karna hai
TARGET_KEYWORDS = ["keyword1", "keyword2"]  # Apne keywords yahan daal dein

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.on_message()
async def forward_filtered_messages(client, message):
    try:
        chat_id = message.chat.id if message.chat else None
        if chat_id in SOURCE_GROUP_IDS:
            if message.text:
                text_clean = message.text.strip()
                text_lower = text_clean.lower()
                
                # '3' ya '4' se shuru hone wale messages ya lines ko yahin rok diya jayega
                if text_lower.startswith(("3", "4")) or any(line.strip().startswith(("3", "4")) for line in text_clean.split("\n")):
                    return
                
                # Agar keywords match karte hain toh message forward hoga
                if any(kw in text_lower for kw in TARGET_KEYWORDS):
                    await client.send_message(TARGET_GROUP_ID, message.text)
                    print("[🚀] Message successfully forward ho gaya!")
    except Exception as e:
        pass

if __name__ == "__main__":
    print("========================================")
    print("   🚀 LIVE FORWARDER USERBOT READY 🚀   ")
    print("========================================")
    app.run()
