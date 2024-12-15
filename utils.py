import logging

logger = logging.getLogger(__name__)

async def delete_message(context):
    try:
        job_context = context.job.context
        chat_id = job_context["chat_id"]
        message_id = job_context["message_id"]

        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Deleted message {message_id} from chat {chat_id}")
    except Exception as e:
        logger.error(f"Error deleting message: {e}")
