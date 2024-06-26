from loguru import logger
from prefect import flow, task

from src.app.collector import Collector
from src.app.loader import pg_manager


@task
def fetch_data():
    collector = Collector()
    # TODO: add theme of article
    articles = collector.fetch_arxiv_papers("machine learning", max_results=2)
    logger.info("Collected articles successfully.")
    return articles


@task
def load_to_db(articles):
    pg_manager.insert_data(articles)
    logger.info("Loaded articles into the database successfully.")
    return True


@flow
def weekly_data_collection_flow():
    articles = fetch_data()
    load_to_db(articles)
    logger.success("Inserted new articles into the database.")


if __name__ == "__main__":
    weekly_data_collection_flow.serve(
        name="ArXiv Data Collector", tags=["arxiv"], cron="31 21 * * *"
    )
