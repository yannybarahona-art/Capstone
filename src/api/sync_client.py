import requests


class SyncClient:
    def __init__(self, url="https://openlibrary.org"):
        self.base_url = url

    def get_works_by_subject(self, subject, pages):
        url = f"{self.base_url}/search.json"
        params = {"q": subject, "page": pages}
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def search_books_by_author(self, query):
        url = f"{self.base_url}/search.json"
        params = {"q": query}
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def search_books_by_author_id(self, query):
        url = f"{self.base_url}/authors/{query}/works.json"
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def search_books_by_title(self, query):
        url = f"{self.base_url}/search.json"
        params = {"q": query}
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def search_books_by_isbn(self, query):
        url = f"{self.base_url}/search.json"
        params = {"q": query}
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
