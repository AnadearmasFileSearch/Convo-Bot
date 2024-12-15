import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import start, forward_message_to_admin, reply_to_user, broadcast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Create the application with the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message_to_admin))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, reply_to_user))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Delete any existing webhook and set the new one
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)

    # Start the webhook
    await application.run_webhook(listen="0.0.0.0", port=80, url_path=WEBHOOK_URL)

if __name__ == '__main__':
    import asyncio
    # Instead of asyncio.run(), directly call the async function
    asyncio.get_event_loop().run_until_complete(main())
