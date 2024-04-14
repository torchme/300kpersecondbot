from src.dags.collector_dag import run_collector
from sender_dag import run_sender


def main():
    run_collector()
    run_sender()


if __name__ == "__main__":
    main()
