import pandas as pd

from src.processing.analytics import DataProcessor


def test_get_key_metrics():
    dataframe = pd.DataFrame(
        {
            "isbn": [
                "978-84-08-24008-2",
                "978-00-00-12345-6",
                "978-12-34-56789-0",
            ],
            "title": [
                "Cien años de soledad",
                "The Hobbit",
                "Don Quijote",
            ],
            "author": [
                "Gabriel García Márquez",
                "J.R.R. Tolkien",
                "Miguel de Cervantes",
            ],
            "publication_year": [
                1967,
                1937,
                1605,
            ],
            "language": [
                "Spanish",
                "English",
                "Spanish",
            ],
        }
    )

    processor = DataProcessor("data/test.db")

    metrics = processor.get_key_metrics(dataframe)

    assert metrics["total_books"] == 3
    assert metrics["unique_authors"] == 3
    assert metrics["unique_isbns"] == 3
    assert metrics["total_languages"] == 2


def test_get_top_publication_years():
    dataframe = pd.DataFrame(
        {
            "publication_year": [
                2020,
                2020,
                2020,
                2021,
                2021,
                2022,
            ]
        }
    )

    processor = DataProcessor("data/test.db")

    result = processor.get_top_publication_years(dataframe)

    assert result.iloc[0]["publication_year"] == 2020
    assert result.iloc[0]["count"] == 3

    assert result.iloc[1]["publication_year"] == 2021
    assert result.iloc[1]["count"] == 2

    assert result.iloc[2]["publication_year"] == 2022
    assert result.iloc[2]["count"] == 1


def test_get_top_languages():
    dataframe = pd.DataFrame(
        {
            "language": [
                "English",
                "English",
                "English",
                "Spanish",
                "Spanish",
                "French",
            ]
        }
    )

    processor = DataProcessor("data/test.db")

    result = processor.get_top_languages(dataframe)

    assert result.iloc[0]["language"] == "English"
    assert result.iloc[0]["count"] == 3

    assert result.iloc[1]["language"] == "Spanish"
    assert result.iloc[1]["count"] == 2

    assert result.iloc[2]["language"] == "French"
    assert result.iloc[2]["count"] == 1
