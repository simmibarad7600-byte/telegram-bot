from pyrogram import Client, filters
from collections import deque

# 1. Aapki API Details
API_ID = 8391628
API_HASH = "85d7a5e61b4054a8f29755a6172e45bf"

# 2. Group IDs (Jahan se messages aayenge)
SOURCE_GROUP_IDS = [
    -1001650537937,   
    -1003933792726,   
    -1004438106656,   
    -1001491105566    
] 

# Aapka Target Group (Jahan receive honge)
TARGET_GROUP_ID = -1001896213793

# 3. Naye Filter Keywords (Country aur 5 series)
TARGET_KEYWORDS = [
    "united states", 
    "france", 
    "spain", 
    "germany", 
    "5 series"
]

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

# Bot ko pichle 50 messages yaad rakhne ke liye ek 'memory' de rahe hain
recent_messages = deque(maxlen=50)

print("==================================================")
print("        🚀 LIVE FORWARDER USERBOT READY 🚀        ")
print("==================================================")
print("Intezaar kar raha hai aapke keywords wale naye messages ka...\n")

@app.on_message(filters.chat(SOURCE_GROUP_IDS))
def auto_forwarder(client, message):
    if message.text:
        text_lower = message.text.lower()
        
        # Check karega ki kya message mein koi bhi ek keyword match hota hai
        if any(keyword in text_lower for keyword in TARGET_KEYWORDS):
            
            # Duplicate Check: Agar text pehle se memory mein NAHI hai, tabhi aage badho
            if message.text not in recent_messages:
                print("[✅] Kaam ka naya message mila! Forward kar raha hoon...")
                
                try:
                    client.send_message(TARGET_GROUP_ID, message.text)
                    # Message bhejne ke baad usko memory mein save kar lo
                    recent_messages.append(message.text)
                    print("[🚀] Message successfully aapke group mein bhej diya gaya!")
                except Exception as e:
                    print(f"[❌] Message bhejne mein error: {e}")
                
                print("-" * 50)
            else:
                print("[⚠️] Yeh message pehle aa chuka hai (Duplicate). Ignore kar diya.")

app.run()
