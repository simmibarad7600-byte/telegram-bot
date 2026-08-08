import os
import re
import time
from pyrogram import Client
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

# Jahan approved Mastercard messages bhejne hain
TARGET_CHAT = -1001896213793

ALLOWED_COUNTRIES = [
    "united states",
    "usa",
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


def extract_unique_identifier(text: str) -> str:
    text_lower = text.lower()
    numbers = "".join(re.findall(r'\d+', text_lower))

    if len(numbers) > 4:
        return numbers[-10:]

    return re.sub(r'[^a-zA-Z0-9]', '', text_lower)


# 🔑 YE SABSE IMPORTANT FIX HAI: Bot start hote hi saari chats/channels ko cache kar lega
@app.on_ready()
async def on_ready(client: Client, *args):
    print("🔄 Loading chats and channels into cache for auto-detection...")
    async for dialog in client.get_dialogs():
        pass
    print("✅ All chats cached successfully! Ready to catch automatic messages.")


@app.on_message()
async def forward_messages(client: Client, message: Message):

    # Target channel ka message dobara process mat karo
    if message.chat and message.chat.id == TARGET_CHAT:
        return

    text = message.text or message.caption or ""

    if not text:
        return

    text_lower = text.lower()

    # 1. Approved check
    if "approved" not in text_lower:
        return

    # 2. Mastercard check
    if not is_mastercard(text):
        return

    # 3. Country check
    is_allowed_country = any(
        country in text_lower
        for country in ALLOWED_COUNTRIES
    )

    if not is_allowed_country:
        return

    current_time = time.time()
    identifier = extract_unique_identifier(text)

    if not identifier or len(identifier) < 4:
        return

    # Old duplicate records remove
    expired_keys = [
        key
        for key, timestamp in sent_transactions.items()
        if current_time - timestamp > TIME_WINDOW
    ]

    for key in expired_keys:
        del sent_transactions[key]

    # Same transaction already forwarded check
    if identifier in sent_transactions:
        print(f"⏩ Duplicate Mastercard transaction blocked: {identifier}")
        return

    try:
        await message.forward(chat_id=TARGET_CHAT)

        sent_transactions[identifier] = current_time

        print(
            f"✅ AUTO-DETECTED & FORWARDED | "
            f"Source: {message.chat.title if message.chat else 'Unknown'}"
        )

    except Exception as e:
        print(f"❌ Forwarding error: {e}")


if __name__ == "__main__":
    print("==========================================")
    print("🚀 FIXED AUTO-DETECT MASTERCARD BOT READY 🚀")
    print("==========================================")
    app.run()
