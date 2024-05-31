import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, Updater
from handlers import start, help_command, custom_command, button, balance, claim_money, echo
import nest_asyncio
import asyncio


# Apply nest_asyncio to allow nested asyncio loops
nest_asyncio.apply()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main() -> None:
    """Start the bot."""
    token = '7083835012:AAE5JIjFteFg1CF3-f9klrV2E56QY43W-OQ'
    application = ApplicationBuilder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("claim", claim_money))

    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Register callback query handler
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Keep the bot running
    while True:
        await asyncio.sleep(60)  # Sleep for 60 seconds to keep the event loop running





if __name__ == '__main__':
    asyncio.run(main())

