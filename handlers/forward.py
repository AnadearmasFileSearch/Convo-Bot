# handlers/forward.py
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from pymongo import MongoClient
from config import MONGO_URL

# Database setup
client = MongoClient(MONGO_URL)
db = client.telegram_bot
messages_collection = db.messages  # Collection to store user-admin message mappings

# Save the mapping between user messages and admin replies
def save_message_mapping(user_id, user_message, admin_message_id):
    messages_collection.insert_one({
        "user_id": user_id,
        "user_message": user_message,
        "admin_message_id": admin_message_id
    })

# Forward user message to admin
async def forward_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    # Forward the message to the admin
    forwarded_message = f"Message from {user_name} (ID: {user_id}):\n{user_message}"
    admin_msg = await context.bot.send_message(chat_id=ADMIN_ID, text=forwarded_message)

    # Save the mapping in the database
    save_message_mapping(user_id, user_message, admin_msg.message_id)
