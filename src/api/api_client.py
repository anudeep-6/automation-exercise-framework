"""
APIClient — base HTTP client wrapping requests.Session.

Mirrors the role of BasePage in the UI layer: all API interactions
go through this class so headers, base URL, and session lifecycle
are managed in one place.
"""

import logging

import requests

logger = logging.getLogger(__name__)


class APIClient:
    """
    Thin wrapper around requests.Session providing a consistent
    interface for all API test interactions.

    Using a Session (rather than bare requests.get / requests.post)
    gives us:
      - Connection pooling across calls in the same test
      - A single place to set shared headers or auth tokens later
      - Easy hook points for retry logic or logging middleware

    Args:
        base_url: Root URL of the API under test, without a trailing slash
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        logger.debug("APIClient initialised with base_url=%s", self.base_url)

    def _url(self, path: str) -> str:
        """Prepend base_url to a relative path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _log_response(self, response: requests.Response) -> None:
        logger.info(
            "%s %s %s in %.0fms",
            response.request.method,
            response.url,
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )

    def get(self, path: str, **kwargs) -> requests.Response:
        """
        Send a GET request to base_url + path.

        Args:
            path: Relative endpoint path, e.g. "/api/productsList"
            **kwargs: Passed directly to requests.Session.get
                      (params, headers, timeout, …)

        Returns:
            requests.Response
        """
        response = self.session.get(self._url(path), **kwargs)
        self._log_response(response)
        return response

    def post(self, path: str, **kwargs) -> requests.Response:
        """
        Send a POST request to base_url + path.

        Args:
            path: Relative endpoint path
            **kwargs: Passed directly to requests.Session.post
                      (data, json, headers, …)

        Returns:
            requests.Response
        """
        response = self.session.post(self._url(path), **kwargs)
        self._log_response(response)
        return response

    def put(self, path: str, **kwargs) -> requests.Response:
        """
        Send a PUT request to base_url + path.

        Args:
            path: Relative endpoint path
            **kwargs: Passed directly to requests.Session.put
                      (data, json, headers, …)

        Returns:
            requests.Response
        """
        response = self.session.put(self._url(path), **kwargs)
        self._log_response(response)
        return response

    def delete(self, path: str, **kwargs) -> requests.Response:
        """
        Send a DELETE request to base_url + path.

        Args:
            path: Relative endpoint path
            **kwargs: Passed directly to requests.Session.delete
                      (headers, …)

        Returns:
            requests.Response
        """
        response = self.session.delete(self._url(path), **kwargs)
        self._log_response(response)
        return response

    def close(self) -> None:
        """Close the underlying session and release connections."""
        self.session.close()
        logger.debug("APIClient session closed")
