from src.db.manager import DatabaseManager


def test_create_tables(tmp_path):
    database_path = tmp_path / "test_library.db"

    database = DatabaseManager(database_path)
    database.create_tables()

    assert database_path.exists()


def test_upsert_many(tmp_path):
    database_path = tmp_path / "test_library.db"

    database = DatabaseManager(database_path)
    database.create_tables()

    entries = [
        {
            "isbn": "978-84-08-24008-2",
            "title": "Test Book",
            "author": "Test Author",
            "publication_year": 2020,
            "language": "English",
        }
    ]

    processed = database.upsert_many(entries)

    works = database.get_all_works()

    assert processed == 1
    assert len(works) == 1

    assert works[0][1] == "978-84-08-24008-2"
    assert works[0][2] == "Test Book"
    assert works[0][3] == "Test Author"


def test_upsert_updates_existing_work(tmp_path):
    database_path = tmp_path / "test_library.db"

    database = DatabaseManager(database_path)
    database.create_tables()

    original_entry = [
        {
            "isbn": "978-84-08-24008-2",
            "title": "Original Title",
            "author": "Original Author",
            "publication_year": 2020,
            "language": "English",
        }
    ]

    updated_entry = [
        {
            "isbn": "978-84-08-24008-2",
            "title": "Updated Title",
            "author": "Updated Author",
            "publication_year": 2024,
            "language": "Spanish",
        }
    ]

    database.upsert_many(original_entry)
    database.upsert_many(updated_entry)

    works = database.get_all_works()

    # There should still be only one record
    assert len(works) == 1

    # Verify that the existing record was updated
    assert works[0][1] == "978-84-08-24008-2"
    assert works[0][2] == "Updated Title"
    assert works[0][3] == "Updated Author"
