import os
from pyrogram import Client, filters

API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Yahan aapke IDs aur saare group/channel names hain
SOURCE_SOURCES = [
    -1001650537937,
    "Savage Scraper",
    "approved_card4",
    "WarnisxCcScrap"
]

TARGET_GROUP_ID = -1001896213793

# Sirf inhi 4 countries ke messages aayenge
TARGET_COUNTRIES = [
    "united states",
    "france",
    "spain",
    "italy"
]

if SESSION_STRING:
    app = Client(
        "my_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )
else:
    app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

@app.on_message()
async def forward_filtered_messages(client, message):
    try:
        if not message.chat:
            return
            
        chat_id = message.chat.id
        chat_title = message.chat.title if message.chat.title else ""
        chat_username = message.chat.username if message.chat.username else ""
        
        # Check karna ki message inhi source groups/channels se hai ya nahi
        is_match = False
        for src in SOURCE_SOURCES:
            if isinstance(src, int) and chat_id == src:
                is_match = True
                break
            elif isinstance(src, str):
                if (chat_username and src.lower() in chat_username.lower()) or (chat_title and src.lower() in chat_title.lower()):
                    is_match = True
                    break
                    
        if is_match:
            if message.text:
                text_clean = message.text.strip()
                
                # Message ki lines check karna ('3' ya '4' se shuru hone wali hatana)
                lines = text_clean.split("\n")
                filtered_lines = []
                
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line.startswith(("3", "4")):
                        continue
                    filtered_lines.append(line)
                
                if not filtered_lines:
                    return
                    
                final_text = "\n".join(filtered_lines)
                final_lower = final_text.lower()
                
                # Sirf tabhi forward karega jab in 4 countries mein se koi ek message mein hogi
                if any(country in final_lower for country in TARGET_COUNTRIES):
                    print(f"[✅] Sahi country ka message mila! Forward kar raha hoon...")
                    await client.send_message(TARGET_GROUP_ID, final_text)
                    print(f"[🚀] Message successfully target group mein bhej diya gaya!")
                    print("-" * 50)
    except Exception as e:
        pass

if __name__ == "__main__":
    print("========================================")
    print("    🚀 LIVE FORWARDER USERBOT READY 🚀    ")
    print("========================================")
    app.run()
