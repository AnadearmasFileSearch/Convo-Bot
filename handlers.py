from config import ADMIN_ID
from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.telegram_bot
messages_collection = db.messages  # Collection to store user-admin message mappings

def save_message_mapping(user_id, user_message, admin_message_id):
    """Save the mapping between user messages and admin replies."""
    messages_collection.insert_one({
        "user_id": user_id,
        "user_message": user_message,
        "admin_message_id": admin_message_id
    })

async def forward_message_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward user messages to the admin."""
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    # Forward the message to the admin
    forwarded_message = f"Message from {user_name} (ID: {user_id}):\n{user_message}"
    admin_msg = await context.bot.send_message(chat_id=ADMIN_ID, text=forwarded_message)

    # Save the mapping in the database
    save_message_mapping(user_id, user_message, admin_msg.message_id)

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin replies to user messages."""
    if update.effective_user.id != ADMIN_ID:
        return  # Only the admin can reply

    # Admin's reply
    reply_message = update.message.text

    # Retrieve the original user ID from the database
    mapping = messages_collection.find_one({"admin_message_id": update.message.reply_to_message.message_id})
    if not mapping:
        await context.bot.send_message(chat_id=ADMIN_ID, text="Cannot find the user to reply to.")
        return

    user_id = mapping['user_id']
    try:
        # Send the reply to the user
        await context.bot.send_message(chat_id=user_id, text=f"Reply from admin: {reply_message}")
    except Exception as e:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Failed to send reply. Error: {e}")
