from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from utils import delete_message, delete_reply
from pymongo import MongoClient
from datetime import timedelta

# Database setup
from config import MONGO_URL
client = MongoClient(MONGO_URL)
db = client.telegram_bot
users_collection = db.users

# Save or update user in the database
def save_user(user_id, username):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "username": username}},
        upsert=True
    )

# Forward message from user to admin
async def forward_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    save_user(user_id, user_name)  # Save user details in the database

    forwarded_message = f"Message from {user_name} (ID: {user_id}):\n{user_message}"
    forwarded_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=forwarded_message,
    )

    # Store message details for later reply
    context.user_data['forwarded_message_id'] = forwarded_msg.message_id
    context.user_data['user_chat_id'] = update.effective_chat.id

# Admin replies to user
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        return  # Only admin can reply

    if 'forwarded_message_id' not in context.user_data:
        return  # No forwarded message to reply to

    reply_message = update.message.text
    user_chat_id = context.user_data['user_chat_id']

    try:
        sent_reply = await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"Reply from admin: {reply_message}"
        )

        # Schedule deletion of the reply message after 2 hours
        context.job_queue.run_once(delete_reply, timedelta(hours=2), context=sent_reply)
    except Exception as e:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Failed to send reply to user. Reason: {e}"
        )

# Admin broadcasts message to all users
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
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

# Command: /users (Admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("Unauthorized! Admins only.")
        return

    count = users_collection.count_documents({})
    await update.message.reply_text(f"Total users: {count}")
