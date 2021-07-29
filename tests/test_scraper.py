import pytest
from unittest.mock import patch
from starlette import status

from app.services.scraper import ScraperService
from tests.test_cases import test_scraper_data


@patch("requests.get")
@pytest.mark.parametrize("test_case", test_scraper_data)
def test_run_and_get_word_count(mock_request, test_case):
    s = ScraperService("https://example.com", test_case["word"])
    mock_request.return_value.content = test_case["content"]
    mock_request.return_value.status_code = status.HTTP_200_OK
    count = s.run_and_get_word_count()
    assert count == test_case["count"]
