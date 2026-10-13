import sqlite3
from pathlib import Path

import pandas as pd


class DataProcessor:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def load_works(self) -> pd.DataFrame:
        sql = """
        SELECT
            isbn,
            title,
            author,
            publication_year,
            language
        FROM works;
        """

        with sqlite3.connect(self.database_path) as connection:
            dataframe = pd.read_sql_query(sql, connection)

        return dataframe

    def clean_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()

        # Remove rows without essential information
        dataframe = dataframe.dropna(subset=["title", "author", "isbn"])

        # Clean text fields
        dataframe["title"] = dataframe["title"].str.strip()
        dataframe["author"] = dataframe["author"].str.strip()
        dataframe["language"] = dataframe["language"].str.strip()

        # Convert publication year to numeric
        dataframe["publication_year"] = pd.to_numeric(
            dataframe["publication_year"], errors="coerce"
        )

        # Remove duplicated ISBNs
        dataframe = dataframe.drop_duplicates(subset=["isbn"])

        return dataframe

    def get_top_publication_years(
        self, dataframe: pd.DataFrame, limit: int = 5
    ) -> pd.DataFrame:

        return (
            dataframe["publication_year"]
            .dropna()
            .value_counts()
            .head(limit)
            .reset_index()
        )

    def get_top_languages(
        self, dataframe: pd.DataFrame, limit: int = 5
    ) -> pd.DataFrame:

        return dataframe["language"].dropna().value_counts().head(limit).reset_index()

    def get_key_metrics(self, dataframe: pd.DataFrame) -> dict:
        return {
            "total_books": len(dataframe),
            "unique_authors": dataframe["author"].nunique(),
            "unique_isbns": dataframe["isbn"].nunique(),
            "total_languages": dataframe["language"].nunique(),
        }
