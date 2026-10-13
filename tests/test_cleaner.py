from src.processing.cleaner import DataCleaner


def test_valid_isbn10():
    result = DataCleaner.is_valid_isbn("1234567890")

    assert result == "Valid ISBN-10"


def test_valid_isbn13():
    result = DataCleaner.is_valid_isbn("978-84-08-24008-2")

    assert result == "Valid ISBN-13"


def test_isbn_too_short():
    result = DataCleaner.is_valid_isbn("123456789")

    assert result == "Invalid ISBN: Too short"


def test_isbn_too_long():
    result = DataCleaner.is_valid_isbn("12345678901234")

    assert result == "Invalid ISBN: Too long"


def test_empty_isbn():
    result = DataCleaner.is_valid_isbn(None)

    assert result == "Empty value is not allowed"


def test_valid_text_input():
    result = DataCleaner.is_valid_isbn("Gabriel Garcia Marquez")

    assert result == "Valid text input"


def test_is_valid_isbn13():
    result = DataCleaner.is_valid_isbn13("978-84-08-24008-2")

    assert result is True
