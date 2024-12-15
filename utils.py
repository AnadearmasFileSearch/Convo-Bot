# Utility functions like deleting messages after a delay

async def delete_message(context):
    """Delete the message after a certain time."""
    try:
        message = context.job.context
        await context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        print(f"Deleted message {message.message_id}")
    except Exception as e:
        print(f"Failed to delete message: {e}")

async def delete_reply(context):
    """Delete the reply message after a certain time."""
    try:
        message = context.job.context
        await context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        print(f"Deleted reply message {message.message_id}")
    except Exception as e:
        print(f"Failed to delete reply: {e}")
