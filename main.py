import os
import re
import time
import traceback
from pyrogram import Client, filters, idle
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
    cards = re.findall(r'\b\d{12,19}\b', text)
    if cards:
        return cards[0]
    
    numbers = "".join(re.findall(r'\d+', text))
    if len(numbers) >= 6:
        return numbers
        
    return str(hash(text))


# 🧪 TESTING COMMAND
@app.on_message(filters.me & filters.command("test", prefixes="."))
async def test_filters_command(client: Client, message: Message):
    test_text = message.text.replace(".test", "").strip()
    if not test_text:
        await message.edit("❌ Kripya test text bhi dein.\nExample: `.test Approved 515828|12|28|123`")
        return
    
    text_lower = test_text.lower()
    has_approved = "approved" in text_lower or "✅" in test_text
    
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
            await client.send_message(TARGET_CHAT, f"[TEST MESSAGE]\n{test_text}")
            print("✅ Test message successfully sent to target chat!")
        except Exception as e:
            print(f"❌ Test send error: {e}")
    else:
        report += "\n❌ **Result:** Text me 'approved' ya '✅' nahi hai!"
        await message.edit(report)


# Main Incoming Message Listener
@app.on_message()
async def forward_messages(client: Client, message: Message):
    try:
        chat_title = message.chat.title if message.chat else "Private"
        chat_id = message.chat.id if message.chat else message.from_user.id
        
        if chat_id == TARGET_CHAT:
            return

        text = message.text or message.caption or ""
        
        if not text:
            return

        text_lower = text.lower()

        # Ab yeh "approved" ya green tick "✅" dono me se kisi ko bhi pakad lega
        if "approved" not in text_lower and "✅" not in text:
            return

        print(f"📥 APPROVED MATCHED in [{chat_title}]! Text length: {len(text)}")

        current_time = time.time()
        identifier = extract_unique_identifier(text)

        expired_keys = [
            key
            for key, timestamp in sent_transactions.items()
            if current_time - timestamp > TIME_WINDOW
        ]

        for key in expired_keys:
            del sent_transactions[key]

        if identifier in sent_transactions:
            print(f"⏩ Duplicate transaction blocked: {identifier}")
            return

        await client.send_message(chat_id=TARGET_CHAT, text=text)
        sent_transactions[identifier] = current_time
        print(f"✅ SUCCESS: Approved message text sent to target chat!")

    except Exception as e:
        print(f"❌ Error in forward_messages: {e}")
        traceback.print_exc()


async def main():
    await app.start()
    print("==========================================")
    print("🚀 FINAL FIXED BOT STARTED SUCCESSFULLY 🚀")
    print("==========================================")

    print("🔄 Loading chats and channels into cache...")
    async for dialog in app.get_dialogs():
        pass
    print("✅ All chats cached successfully!")

    await idle()
    await app.stop()


if __name__ == "__main__":
    app.run(main())
