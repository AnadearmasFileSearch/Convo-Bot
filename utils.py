import logging

# Set up logging
logger = logging.getLogger(__name__)

async def delete_message(context):
    """
    Deletes a message from the chat after a specified time.
    """
    try:
        job_context = context.job.context
        chat_id = job_context.get("chat_id")
        message_id = job_context.get("message_id")

        if chat_id and message_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Deleted message {message_id} from chat {chat_id}")
        else:
            logger.error("Missing chat_id or message_id in job context.")
    except Exception as e:
        logger.error(f"Failed to delete message. Error: {e}")

async def delete_reply(context):
    """
    Deletes a reply message after a specified time.
    """
    try:
        job_context = context.job.context
        chat_id = job_context.get("chat_id")
        message_id = job_context.get("message_id")

        if chat_id and message_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Deleted reply message {message_id} from chat {chat_id}")
        else:
            logger.error("Missing chat_id or message_id in job context.")
    except Exception as e:
        logger.error(f"Failed to delete reply. Error: {e}")
