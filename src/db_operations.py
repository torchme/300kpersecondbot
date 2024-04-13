import psycopg2


def create_tables(conn_params):
    try:
        with psycopg2.connect(**conn_params) as conn:
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
                print("Tables created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating tables: {error}")


def insert_data(conn_params, data):
    try:
        with psycopg2.connect(**conn_params) as conn:
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
                    article_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting data: {error}")
        if conn:
            conn.rollback()
