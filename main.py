from flask import Flask, request
import asyncio
from telegram.ext import Application
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import start, forward_message_to_admin, reply_to_user
from utils import delete_message

app = Flask(__name__)

# Initialize the application
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
application.add_handler(MessageHandler(filters.REPLY, reply_to_user))

# Set webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

if __name__ == "__main__":
    application.bot.set_webhook(f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=5000)
