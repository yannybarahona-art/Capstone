import sqlite3

sqlite3.connect("data/open_library.db")

from pathlib import Path


class DatabaseManager:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def create_tables(self) -> None:
        works_sql = """
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER,
            language TEXT
        );
        """

        cache_sql = """
        CREATE TABLE IF NOT EXISTS api_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cache_key TEXT NOT NULL UNIQUE,
            response TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        );
        """

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(works_sql)
            connection.execute(cache_sql)
            connection.commit()

    def upsert_work(
        self,
        author: str,
        title: str,
        isbn: str,
    ) -> None:
        """
        Inserta un libro nuevo o actualiza el existente
        cuando el ISBN ya está registrado.
        """
        sql = """
        INSERT INTO works (
            isbn,
            title,
            author
        )
        VALUES (?, ?, ?)
        ON CONFLICT(isbn)
        DO UPDATE SET
            title = excluded.title,
            author = excluded.author;
        """

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                sql,
                (isbn, title, author),
            )
            connection.commit()

    def upsert_many(self, entries) -> int:

        sql = """
        INSERT INTO works (
            isbn,
            title,
            author,
            publication_year,
            language
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(isbn)
        DO UPDATE SET
            title = excluded.title,
            author = excluded.author,
            publication_year = excluded.publication_year,
            language = excluded.language;
        """

        processed = 0

        with sqlite3.connect(self.database_path) as connection:
            for entry in entries:
                connection.execute(
                    sql,
                    (
                        entry["isbn"],
                        entry["title"],
                        entry["author"],
                        entry["publication_year"],
                        entry["language"],
                    ),
                )

                processed += 1

            connection.commit()

            return processed

    def get_all_works(self) -> list:
        """Obtiene todos los libros almacenados."""
        sql = """
        SELECT id, isbn, title, author
        FROM works
        ORDER BY title;
        """

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(sql)
            return cursor.fetchall()

    def get_database_metrics(self) -> dict:
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            # Total works
            cursor.execute("SELECT COUNT(*) FROM works")
            works_count = cursor.fetchone()[0]

            # Database size in bytes
            database_size = self.database_path.stat().st_size

            return {
                "works_count": works_count,
                "database_size": database_size,
            }

    def purge_expired_cache(self) -> int:
        sql = """
        DELETE FROM api_cache
        WHERE datetime(expires_at) <= datetime('now');
        """

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(sql)
            connection.commit()

            return cursor.rowcount
