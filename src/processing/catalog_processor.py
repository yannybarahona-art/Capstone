import csv
import re
import unicodedata
from collections.abc import Generator
from pathlib import Path


class CatalogProcessor:
    @staticmethod
    def normalize_text(value: str) -> str:
        """
        Normaliza texto Unicode y elimina espacios innecesarios.
        """
        if not value:
            return ""

        normalized = unicodedata.normalize("NFC", value)

        # Elimina espacios al inicio/final y espacios internos duplicados.
        return " ".join(normalized.strip().split())

    @staticmethod
    def normalize_isbn(isbn: str) -> str:
        """
        Elimina espacios externos del ISBN.
        """
        if not isbn:
            return ""

        return isbn.strip()

    @staticmethod
    def is_valid_isbn_format(isbn: str) -> bool:
        """
        Valida el formato XXX-XX-XX-XXXXX-X.
        No valida el checksum.
        """
        pattern = r"\d{3}-\d{2}-\d{2}-\d{5}-\d"
        return bool(re.fullmatch(pattern, isbn))

    @classmethod
    def stream_catalog(
        cls,
        file_path: str | Path,
    ) -> Generator[dict, None, None]:

        file_path = Path(file_path)

        with file_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                yield {
                    "author": cls.normalize_text(row.get("author", "")),
                    "title": cls.normalize_text(row.get("title", "")),
                    "isbn": cls.normalize_isbn(row.get("isbn", "")),
                    "publication_year": cls.normalize_text(
                        row.get("publication_year", "")
                    ),
                    "language": cls.normalize_text(row.get("language", "")),
                }

    @classmethod
    def get_unique_entries(
        cls,
        file_path: str | Path,
    ) -> Generator[dict, None, None]:
        """
        Elimina duplicados usando un set.

        El ISBN se utiliza como identificador único.
        """
        seen_isbns = set()

        for entry in cls.stream_catalog(file_path):
            author = entry["author"]
            title = entry["title"]
            isbn = entry["isbn"]

            if not author or not title or not isbn:
                print(f"Skipped incomplete entry: {entry}")
                continue

            if not cls.is_valid_isbn_format(isbn):
                print(f"Skipped invalid ISBN: {isbn}")
                continue

            if isbn in seen_isbns:
                print(f"Skipped duplicate ISBN: {isbn}")
                continue

            seen_isbns.add(isbn)

            yield entry
