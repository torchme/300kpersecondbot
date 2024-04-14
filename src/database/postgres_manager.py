import datetime

import psycopg2
from loguru import logger


class PostgresManager:
    """
    Postgres manager class.
    """

    def __init__(self, conn_db):
        self.conn_db = conn_db

    def create_tables(self):
        """
        Create tables in the database.
        """
        try:
            with psycopg2.connect(**self.conn_db) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS articles (
                            id SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            summary TEXT,
                            published TIMESTAMP WITH TIME ZONE,
                            link TEXT NOT NULL UNIQUE,
                            h_index FLOAT,
                            i10_index FLOAT
                        );
                        """
                    )
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS authors (
                            id SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            article_id INTEGER,
                            FOREIGN KEY (article_id) REFERENCES articles(id),
                            UNIQUE (name, article_id)
                        );
                        """
                    )
                    conn.commit()
                    logger.success("Tables created successfully.")
        except psycopg2.DatabaseError as error:
            logger.error(f"Error creating tables: {error}")

    def insert_data(self, data):
        """
        Insert data into the database.
        """
        try:
            with psycopg2.connect(**self.conn_db) as conn:
                with conn.cursor() as cursor:
                    for item in data:
                        cursor.execute(
                            """
                            INSERT INTO articles (title, summary, published, link, h_index, i10_index)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (link) DO NOTHING
                            RETURNING id;
                        """,
                            (
                                item["title"],
                                item["summary"],
                                item["published"],
                                item["link"],
                                item["h_index"],
                                item["i10_index"],
                            ),
                        )
                        article_id = (
                            cursor.fetchone()[0] if cursor.rowcount > 0 else None
                        )

                        if article_id:
                            for author in item["authors"]:
                                cursor.execute(
                                    """
                                    INSERT INTO authors (name, article_id) VALUES (%s, %s)
                                    ON CONFLICT (name, article_id) DO NOTHING;
                                """,
                                    (author, article_id),
                                )
                    conn.commit()
        except psycopg2.DatabaseError as error:
            logger.error(f"Error inserting data: {error}")
            if conn:
                conn.rollback()

    def top_articles(self, num_published=10, days=7):
        """
        Fetch top articles by indexes from the database.
        """
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)

        try:
            with psycopg2.connect(**self.conn_db) as conn:
                with conn.cursor() as cursor:
                    query = """
                    SELECT * FROM articles
                    WHERE published BETWEEN %s AND %s
                    ORDER BY i10_index DESC, h_index DESC
                    LIMIT %s;
                    """
                    cursor.execute(query, (start_date, end_date, num_published))
                    articles = cursor.fetchall()
                    logger.success("Fetched articles successfully.")
                    return articles
        except psycopg2.DatabaseError as error:
            logger.error(f"Error fetching articles: {error}")
            return []
