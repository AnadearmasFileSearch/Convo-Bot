import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_URL

from handlers import start, forward_message_to_admin, reply_to_user, broadcast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Create the Application instance with your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, reply_to_user))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Clear any existing webhook to avoid conflicts
    application.bot.delete_webhook()

    # Set the new webhook URL
    application.bot.set_webhook(url=WEBHOOK_URL)

    # Start the bot using webhook instead of polling
    application.run_webhook(listen="0.0.0.0", port=80, url_path=WEBHOOK_URL)

if __name__ == '__main__':
    main()
