import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import start, forward_message_to_admin, reply_to_user, broadcast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, reply_to_user))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Set webhook (if required for deployment)
    application.bot.set_webhook(url=WEBHOOK_URL)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
