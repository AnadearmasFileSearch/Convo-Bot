# handlers/broadcast.py
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from pymongo import MongoClient
from config import MONGO_URL

# Database setup
client = MongoClient(MONGO_URL)
db = client.telegram_bot
users_collection = db.users  # Collection to store user information

# Command: /broadcast (Admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a broadcast message to all users."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <your message>")
        return

    message = " ".join(context.args)
    users = users_collection.find()

    for user in users:
        try:
            await context.bot.send_message(chat_id=user['user_id'], text=message)
        except Exception as e:
            print(f"Failed to send to {user['user_id']}: {e}")

    await update.message.reply_text("Broadcast completed!")
