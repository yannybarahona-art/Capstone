from unittest.mock import Mock, patch

from src.api.sync_client import SyncClient


@patch("src.api.sync_client.requests.get")
def test_search_books_by_author(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "numFound": 1,
        "docs": [
            {
                "title": "The Hobbit",
                "author_name": ["J.R.R. Tolkien"],
            }
        ],
    }

    mock_get.return_value = mock_response

    client = SyncClient()

    result = client.search_books_by_author("Tolkien")

    assert result["numFound"] == 1
    assert result["docs"][0]["title"] == "The Hobbit"
    assert result["docs"][0]["author_name"] == ["J.R.R. Tolkien"]

    mock_response.raise_for_status.assert_called_once()


@patch("src.api.sync_client.requests.get")
def test_search_books_by_author_parameters(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {"numFound": 1, "docs": []}

    mock_get.return_value = mock_response

    client = SyncClient()

    client.search_books_by_author("Tolkien")

    mock_get.assert_called_once_with(
        "https://openlibrary.org/search.json",
        params={"q": "Tolkien"},
        verify=False,
    )

    mock_response.raise_for_status.assert_called_once()
