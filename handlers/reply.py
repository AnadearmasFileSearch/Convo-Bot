from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.telegram_bot
messages_collection = db.messages

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    reply_message = update.message.text
    mapping = messages_collection.find_one({"admin_message_id": update.message.reply_to_message.message_id})

    if not mapping:
        await context.bot.send_message(chat_id=ADMIN_ID, text="Cannot find the user to reply to.")
        return

    user_id = mapping['user_id']
    try:
        await context.bot.send_message(chat_id=user_id, text=f"Reply from admin: {reply_message}")
    except Exception as e:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Failed to send reply. Error: {e}")
