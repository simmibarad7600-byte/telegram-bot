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

sent_transactions = {}
TIME_WINDOW = 900  # 15 minutes


def extract_unique_identifier(text: str) -> str:
    text_lower = text.lower()

    numbers = "".join(re.findall(r'\d+', text_lower))

    if len(numbers) > 4:
        return numbers[-10:]

    return re.sub(r'[^a-zA-Z0-9]', '', text_lower)


@app.on_message()
async def forward_messages(client: Client, message: Message):
    text = message.text or message.caption or ""
    text_lower = text.lower()

    # Approved check
    if "approved" not in text_lower:
        return

    # Country check
    is_allowed = any(
        country in text_lower
        for country in ALLOWED_COUNTRIES
    )

    if is_allowed:
        current_time = time.time()
        identifier = extract_unique_identifier(text)

        if not identifier or len(identifier) < 4:
            return

        # Purane records delete
        expired_keys = [
            k for k, timestamp in sent_transactions.items()
            if current_time - timestamp > TIME_WINDOW
        ]

        for k in expired_keys:
            del sent_transactions[k]

        # Duplicate transaction rokna
        if identifier in sent_transactions:
            print("⏩ Ek hi transaction ka doosra message rok liya gaya!")
            return

        try:
            await message.forward(chat_id=TARGET_CHAT)

            sent_transactions[identifier] = current_time

            print("✅ Pehla approved message successfully forward kiya gaya!")

        except Exception as e:
            print(f"Error forwarding message: {e}")


if __name__ == "__main__":
    print("==========================================")
    print("🚀 SMART TRANSACTION DEDUPLICATOR READY 🚀")
    print("==========================================")
    app.run()
