from aiogram import Bot, Dispatcher, executor, types
from src.config.config import APP_TOKEN
from src.app.postgres_manager import (
    PostgresManager,
)  # Убедитесь, что класс импортирован


class TG_Service:
    def __init__(self):
        self.bot = Bot(token=APP_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.db_manager = PostgresManager()

        # Registering handlers
        self.dp.register_message_handler(self.take_answer)
        self.dp.register_message_handler(self.send_articles, commands=["get_articles"])

    async def take_answer(self, message: types.Message):
        query_text = message.text
        response = f"Your query: {query_text}"
        await message.reply(response)

    async def send_articles(self):
        articles = self.db_manager.fetch_top_articles_by_indexes(n=5)
        if not articles:
            await self.bot.send_message(
                chat_id="your_chat_id", text="No articles found."
            )
            return

        response = "\n\n".join(
            [
                f"Title: {article[1]}\nPublished: {article[3]}\nLink: {article[4]}"
                for article in articles
            ]
        )
        await self.bot.send_message(chat_id="your_chat_id", text=response)

    def run(self):
        """Run application"""
        executor.start_polling(self.dp)


if __name__ == "__main__":
    tg_service = TG_Service()
    tg_service.run()  # This method starts the bot
