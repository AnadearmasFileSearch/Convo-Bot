import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Bot token
TOKEN = "7524278392:AAGd21uCuExw-JAuko9UC5l9GLrqmwy-mh4"
WEBHOOK_URL = "https://convo-bot-4hl6.onrender.com"  # Replace with your actual webhook URL

# Command to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! I am your bot.')

# Main function to set up the webhook
async def main():
    # Create Application instance
    application = Application.builder().token(TOKEN).build()

    # Register the start command
    application.add_handler(CommandHandler("start", start))

    # Run the webhook
    await application.run_webhook(listen="0.0.0.0", port=80, url_path=WEBHOOK_URL)

if __name__ == "__main__":
    # Let Telegram handle the event loop
    import asyncio
    asyncio.run(main())
