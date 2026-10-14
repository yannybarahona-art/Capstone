import re


class DataCleaner:
    @staticmethod
    def clean_text(text):
        pass

    @staticmethod
    def is_valid_isbn(isbn):
        if isbn is None:
            return "Empty value is not allowed"
        if bool(re.fullmatch(r"\d{10}", isbn)):
            return "Valid ISBN-10"
        if not isbn.isdigit() and len(isbn) == 10:
            return "Invalid ISBN-10: Contains non-numeric characters"
        # if bool(re.fullmatch(r"\d{13}", isbn)):
        if re.fullmatch(r"\d{3}-\d{2}-\d{2}-\d{5}-\d", isbn) or re.fullmatch(
            r"\d{13}", isbn
        ):
            return "Valid ISBN-13"
        if not isbn.isdigit() and len(isbn) == 13:
            return "Invalid ISBN-13: Contains non-numeric characters"
        if isbn.isdigit() and len(isbn) < 10:
            return "Invalid ISBN: Too short"
        if isbn.isdigit() and len(isbn) > 13:
            return "Invalid ISBN: Too long"
        if re.fullmatch(r"[A-Za-z ]+", isbn):
            return "Valid text input"

    @staticmethod
    def is_valid_isbn13(isbn):
        return bool(re.fullmatch(r"\d{3}-\d{2}-\d{2}-\d{5}-\d", isbn))
