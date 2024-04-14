from src.dags.collector_dag import weekly_data_collection_flow
from src.dags.sender_dag import article_sender_flow


def init_collector_dag():
    # Инициализация и запуск потока коллектора
    weekly_data_collection_flow()


def init_sender_dag():
    # Инициализация и запуск потока отправителя
    article_sender_flow()


def main():
    # Инициализация всех потоков
    init_collector_dag()
    init_sender_dag()


if __name__ == "__main__":
    main()
