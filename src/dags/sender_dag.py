from aiogram.utils.markdown import hbold, hlink
from loguru import logger
from prefect import flow, task

from src.app.bot import PerSecond300kBot
from src.app.loader import pg_manager
from src.config.config import CHAT_ID

bot_runner = PerSecond300kBot()


@task
async def send_articles_task():
    articles = pg_manager.top_articles(num_published=5, days=7)
    if not articles:
        response = "На этой неделе пока нет статей на ARXIV 😢"
    else:
        response = (
            f"{hbold('📦 ПЯТНИЧНЫЙ ARXIV 📚')}\n\n" "Лучшие статьи за эту неделю:\n"
        )

        for index, article in enumerate(articles, 1):
            title = article[1]
            link = article[4]
            response += f"{index}️⃣ {hlink(title, link)}\n"

        response += (
            f"\n{hlink('🗳 Отдать голос', 'https://t.me/boost/persecond300k')}\n\n"
            f"{hlink('💬 Вступить в чат', 'https://t.me/persecond300kchat')}"
        )
        logger.info(response)
    await bot_runner.send_message(CHAT_ID, response)


@flow
def article_sender_flow():
    send_articles_task()
    logger.success("Articles sent successfully.")


if __name__ == "__main__":
    article_sender_flow.serve(
        name="Telegram Sender Arxiv", tags=["arxiv", "telegram"], cron="55 20 * * *"
    )
