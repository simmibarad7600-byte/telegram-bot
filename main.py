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

ALLOWED_COUNTRIES = [
    "united states",
    "usa",
    "us",
    "france",
    "spain",
    "italy"
]

MASTERCARD_WORDS = [
    "mastercard",
    "master card",
    "master",
    "mc"
]

sent_transactions = {}
TIME_WINDOW = 900  # 15 minutes


def is_mastercard(text: str) -> bool:
    text_lower = text.lower()

    if any(word in text_lower for word in MASTERCARD_WORDS):
        return True

    numbers = re.findall(r'\b\d{6,16}\b', text)

    for number in numbers:
        try:
            prefix2 = int(number[:2])
            prefix4 = int(number[:4])

            if 51 <= prefix2 <= 55:
                return True

            if 2221 <= prefix4 <= 2720:
                return True

        except ValueError:
            pass

    return False


def is_country_allowed(text_lower: str) -> bool:
    for country in ALLOWED_COUNTRIES:
        if len(country) <= 3:
            pattern = r'\b' + re.escape(country) + r'\b'
            if re.search(pattern, text_lower):
                return True
        else:
            if country in text_lower:
                return True
    return False


def extract_unique_identifier(text: str) -> str:
    text_lower = text.lower()
    numbers = "".join(re.findall(r'\d+', text_lower))

    if len(numbers) > 4:
        return numbers[-10:]

    return re.sub(r'[^a-zA-Z0-9]', '', text_lower)


# 🧪 TESTING COMMAND: Apni chat me .test likh kar check kar sakte hain
@app.on_message(filters.me & filters.command("test", prefixes="."))
async def test_filters_command(client: Client, message: Message):
    test_text = message.text.replace(".test", "").strip()
    if not test_text:
        await message.edit("❌ Kripya test text bhi dein.\nExample: `.test Approved Mastercard US 515828|12|28|123`")
        return
    
    text_lower = test_text.lower()
    
    has_approved = "approved" in text_lower
    has_mc = is_mastercard(test_text)
    has_country = is_country_allowed(text_lower)
    
    report = (
        f"🧪 **FILTER TEST REPORT:**\n"
        f"----------------------------------\n"
        f"📝 Text: `{test_text}`\n"
        f"• Approved Check: {'✅ PASS' if has_approved else '❌ FAIL'}\n"
        f"• Mastercard Check: {'✅ PASS' if has_mc else '❌ FAIL'}\n"
        f"• Country Check: {'✅ PASS' if has_country else '❌ FAIL'}\n"
    )
    
    if has_approved and has_mc and has_country:
        report += "\n✨ **Result:** Sabhi filters pass ho gaye! Target chat par bhej raha hu..."
        await message.edit(report)
        try:
            await client.send_message(TARGET_CHAT, f"[TEST MESSAGE] {test_text}")
            print("✅ Test message successfully sent to target chat!")
        except Exception as e:
            print(f"❌ Test send error: {e}")
    else:
        report += "\n❌ **Result:** Filters fail ho gaye! Yeh message live me forward nahi hoga."
        await message.edit(report)


# Main Incoming Message Listener
@app.on_message()
async def forward_messages(client: Client, message: Message):
    if message.chat and message.chat.id == TARGET_CHAT:
        return

    text = message.text or message.caption or ""

    if not text:
        return

    print(f"📥 Message received from [{message.chat.title if message.chat else 'Private'}]: {text[:40]}...")

    text_lower = text.lower()

    if "approved" not in text_lower:
        return

    if not is_mastercard(text):
        return

    if not is_country_allowed(text_lower):
        return

    print("✨ All Filters Passed! Preparing to copy...")

    current_time = time.time()
    identifier = extract_unique_identifier(text)

    if not identifier or len(identifier) < 4:
        return

    expired_keys = [
        key
        for key, timestamp in sent_transactions.items()
        if current_time - timestamp > TIME_WINDOW
    ]

    for key in expired_keys:
        del sent_transactions[key]

    if identifier in sent_transactions:
        print(f"⏩ Duplicate Mastercard transaction blocked: {identifier}")
        return

    try:
        await message.copy(chat_id=TARGET_CHAT)
        sent_transactions[identifier] = current_time
        print(f"✅ SUCCESS: Message copied & sent to target chat!")
    except Exception as e:
        print(f"❌ Copying error: {e}")


async def main():
    await app.start()
    print("==========================================")
    print("🚀 AUTO-DETECT MASTERCARD BOT READY 🚀")
    print("==========================================")

    print("🔄 Loading chats and channels into cache for auto-detection...")
    async for dialog in app.get_dialogs():
        pass
    print("✅ All chats cached successfully! Ready to catch automatic messages.")

    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
