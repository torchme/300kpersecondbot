import asyncio

from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand
from loguru import logger

from src.app.loader import bot, dp


class PerSecond300kBot:
    def __init__(self):
        dp.startup.register(self.startup_event)
        dp.shutdown.register(self.shutdown_event)

    async def start(self):
        """
        Starts the bot by polling the dispatcher.
        """
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)

    async def startup_event(self):
        """
        An asynchronous function to handle the startup event
        """
        bot_commands = [
            BotCommand(command="/help", description="ℹ️ About me"),
        ]
        await bot.set_my_commands(bot_commands)
        logger.warning("Bot started")

    async def send_message(self, chat_id, response):
        """
        Asynchronous function to send articles to the user.
        """
        await bot.send_message(chat_id, response)
        logger.info("Sending articles")

    async def shutdown_event(self):
        """
        Asynchronous function to handle the shutdown event of the bot.
        """
        logger.warning("Bot stopped")


if __name__ == "__main__":
    bot_runner = PerSecond300kBot()
    asyncio.run(bot_runner.start())
