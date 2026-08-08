import os
import re
import time
from pyrogram import Client, idle, filters
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

sent_transactions = {}
TIME_WINDOW = 900  # 15 minutes


def extract_unique_identifier(text: str) -> str:
    # Message me se exact card number (12 se 19 digits) dhoondho taaki har card ki unique ID bane
    cards = re.findall(r'\b\d{12,19}\b', text)
    if cards:
        return cards[0]
    
    # Agar card number na mile toh saare numbers ka combination use karo
    numbers = "".join(re.findall(r'\d+', text))
    if len(numbers) >= 6:
        return numbers
        
    # Agar numbers bhi na ho toh poore message ka hash use karo taaki 'approved' word ki wajah se block na ho
    return str(hash(text))


# 🧪 TESTING COMMAND
@app.on_message(filters.me & filters.command("test", prefixes="."))
async def test_filters_command(client: Client, message: Message):
    test_text = message.text.replace(".test", "").strip()
    if not test_text:
        await message.edit("❌ Kripya test text bhi dein.\nExample: `.test Approved 515828|12|28|123`")
        return
    
    text_lower = test_text.lower()
    has_approved = "approved" in text_lower
    
    report = (
        f"🧪 **TEST REPORT:**\n"
        f"----------------------------------\n"
        f"📝 Text: `{test_text}`\n"
        f"• Approved Check: {'✅ PASS' if has_approved else '❌ FAIL'}\n"
    )
    
    if has_approved:
        report += "\n✨ **Result:** Approved mil gaya! Target chat par bhej raha hu..."
        await message.edit(report)
        try:
            await client.send_message(TARGET_CHAT, f"[TEST MESSAGE] {test_text}")
            print("✅ Test message successfully sent to target chat!")
        except Exception as e:
            print(f"❌ Test send error: {e}")
    else:
        report += "\n❌ **Result:** Text me 'approved' nahi hai!"
        await message.edit(report)


# Main Incoming Message Listener
@app.on_message()
async def forward_messages(client: Client, message: Message):
    if message.chat and message.chat.id == TARGET_CHAT:
        return

    text = message.text or message.caption or ""

    if not text:
        return

    text_lower = text.lower()

    if "approved" not in text_lower:
        return

    print(f"📥 Approved message received from [{message.chat.title if message.chat else 'Private'}]: {text[:40]}...")

    current_time = time.time()
    identifier = extract_unique_identifier(text)

    # Purane entries saaf karein
    expired_keys = [
        key
        for key, timestamp in sent_transactions.items()
        if current_time - timestamp > TIME_WINDOW
    ]

    for key in expired_keys:
        del sent_transactions[key]

    # Duplicate check (Ab yeh sirf same exact card/message ko hi rogega)
    if identifier in sent_transactions:
        print(f"⏩ Duplicate transaction blocked: {identifier}")
        return

    try:
        await message.copy(chat_id=TARGET_CHAT)
        sent_transactions[identifier] = current_time
        print(f"✅ SUCCESS: Approved message copied & sent to target chat!")
    except Exception as e:
        print(f"❌ Copying error: {e}")


async def main():
    await app.start()
    print("==========================================")
    print("🚀 FIXED AUTO-DETECT BOT READY 🚀")
    print("==========================================")

    print("🔄 Loading chats and channels into cache...")
    async for dialog in app.get_dialogs():
        pass
    print("✅ All chats cached successfully!")

    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
