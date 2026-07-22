import os
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

SOURCE_GROUP_IDS = [-1001234567890]  # Apni source group ID daalein
TARGET_GROUP_ID = -1009876543210    # Apni target group ID daalein
TARGET_KEYWORDS = ["keyword1", "keyword2"]  # Apne keywords daalein

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
                
                # Message ki har ek line ko check karenge
                lines = text_clean.split("\n")
                filtered_lines = []
                
                for line in lines:
                    stripped_line = line.strip()
                    # Agar line '3' ya '4' se shuru hoti hai, toh use bilkul mat lo (skip kar do)
                    if stripped_line.startswith(("3", "4")):
                        continue
                    filtered_lines.append(line)
                
                # Agar saari hi lines nikal gayin, toh message mat bhejo
                if not filtered_lines:
                    return
                    
                final_text = "\n".join(filtered_lines)
                final_lower = final_text.lower()
                
                # Baaki bache hue text me keyword match hone par hi forward karega
                if any(kw in final_lower for kw in TARGET_KEYWORDS):
                    await client.send_message(TARGET_GROUP_ID, final_text)
                    print("[🚀] Cleaned message successfully forward ho gaya!")
    except Exception as e:
        pass

if __name__ == "__main__":
    print("========================================")
    print("   🚀 LIVE FORWARDER USERBOT READY 🚀   ")
    print("========================================")
    app.run()
