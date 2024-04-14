from prefect import flow, task
from prefect.schedules import IntervalSchedule
from datetime import timedelta
from src.app.collector import Collector
from src.database.postgres_manager import PostgresManager


@task
def fetch_data():
    collector = Collector()
    # Предполагается, что вы ищете статьи по конкретной теме, например 'machine learning'
    articles = collector.fetch_arxiv_papers("machine learning", max_results=50)
    return articles


@task
def insert_data(articles):
    manager = PostgresManager()
    manager.insert_data(articles)
    return len(articles)


schedule = IntervalSchedule(interval=timedelta(days=1))


@flow(name="Daily ArXiv Data Collection", schedule=schedule, log_prints=True)
def weekly_data_collection_flow():
    articles = fetch_data()
    num_inserted = insert_data(articles)
    print(f"Inserted {num_inserted} new articles into the database.")


# Регистрация и запуск потока
if __name__ == "__main__":
    weekly_data_collection_flow()
