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
        response = "No articles found."
    else:
        response = "\n\n".join([
            f"Title: {article['title']}\nPublished: {article['date']}\nLink: {article['link']}"
            for article in articles
        ])

    await bot_runner.send_message(CHAT_ID, response)
    logger.info("Articles sent successfully.")


@flow
def article_sender_flow():
    send_articles_task()


if __name__ == "__main__":
    article_sender_flow.serve(
        name="Weekly Article Sender", tags=["arxiv"], cron="55 20 * * *"
    )
