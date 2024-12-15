from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from datetime import timedelta
from pymongo import MongoClient
from config import MONGO_URL

# Database setup
client = MongoClient(MONGO_URL)
db = client.telegram_bot
users_collection = db.users

def save_user(user_id, username):
    """Save or update user information in the database."""
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "username": username}},
        upsert=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "Unknown"
    save_user(chat_id, username)

    # Send welcome photo with buttons
    image_url = "https://i.ibb.co/SB9XZ6Z/photo-2024-12-14-08-27-56-7448181445471764512.jpg"
    keyboard = [
        [InlineKeyboardButton("⚡Movie Link Here", url="https://t.me/Pushpa_Part_2_The_Rule_Tamil/20")],
        [InlineKeyboardButton("🎯Join Our Main Channel", url="https://t.me/FilesUlagam1")],
        [InlineKeyboardButton("🤗Group Link", url="https://t.me/+xR-e38apt6AxMmY1")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent_message = await context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption="Welcome to our Channel!🥳Here👇",
        reply_markup=reply_markup
    )

    # Schedule deletion after 2 minutes
    context.job_queue.run_once(
        delete_message,
        timedelta(minutes=2),
        context={"chat_id": sent_message.chat.id, "message_id": sent_message.message_id}
    )