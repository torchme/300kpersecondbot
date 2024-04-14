from prefect import flow, task
from prefect.schedules import CronSchedule
from src.app.bot import TG_Service  # Импорт вашего класса бота
from datetime import datetime

# Создайте экземпляр бота
tg_service = TG_Service()


@task
def send_articles_task():
    # Имитация вызова команды Telegram бота
    class MockMessage:
        def __init__(self):
            self.text = "/get_articles"

        async def reply(self, text):
            print(text)  # Просто печатаем в консоль вместо отправки в Telegram

    # Так как это асинхронный метод, нужно оборачивать его в asyncio loop
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tg_service.send_articles())


# Настраиваем расписание на каждую пятницу в 09:00
schedule = CronSchedule("0 9 * * 5", start_date=datetime.datetime.now())


@flow(name="Weekly Article Sender", schedule=schedule)
def article_sender_flow():
    send_articles_task()


# Регистрация и запуск flow
if __name__ == "__main__":
    article_sender_flow()
