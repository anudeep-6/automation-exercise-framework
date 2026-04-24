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
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            }
        )
        self._prime_csrf()
        logger.debug(f"APIClient initialised with base_url={self.base_url}")

    def _prime_csrf(self) -> None:
        """
        Fetch the homepage to seed the session cookie jar with a csrftoken,
        then set the headers Django's CSRF middleware requires on HTTPS:
        - X-CSRFToken: validated by Django on AJAX-style requests
        - Referer: required by Django's CSRF middleware on all HTTPS POSTs —
            must match the host or the middleware rejects the request with 403
            regardless of whether the token is present and valid
        """
        self.session.get(self.base_url, timeout=10)
        csrf = self.session.cookies.get("csrftoken")
        if csrf:
            self.session.headers.update(
                {
                    "X-CSRFToken": csrf,
                    "Referer": f"{self.base_url}/",
                }
            )
            logger.debug("CSRF token primed and Referer header set")
        else:
            logger.warning("No csrftoken found on homepage — API write calls may 403")

    def _url(self, path: str) -> str:
        """Prepend base_url to a relative path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _log_response(self, response: requests.Response) -> None:
        elapsed_ms = response.elapsed.total_seconds() * 1000 if response.elapsed else 0
        msg = (
            f"{response.request.method} {response.url} | Status: "
            f"{response.status_code} | Time: {elapsed_ms:.0f}ms"
        )
        if response.status_code >= 400:
            logger.error(msg)
            logger.error(f"Response body:\n{response.text[:500]}")
        elif response.is_redirect:
            logger.warning(
                f"{msg} → redirecting to: {response.headers.get('Location', 'unknown')}"
            )
        else:
            logger.info(msg)

    def get(self, path: str, **kwargs) -> requests.Response:
        """
        Send a GET request to base_url + path.

        Args:
            path: Relative endpoint path, e.g. "/api/productsList"
            **kwargs: Passed directly to requests.Session.get

        Returns:
            requests.Response — redirect responses are returned as-is;
            callers receive the raw API response, not the redirect target.
        """
        logger.debug(f"GET {self._url(path)}")
        response = self.session.get(self._url(path), allow_redirects=False, **kwargs)
        self._log_response(response)
        return response

    def post(self, path: str, **kwargs) -> requests.Response:
        """
        Send a POST request to base_url + path.

        Args:
            path: Relative endpoint path
            **kwargs: Passed directly to requests.Session.post

        Returns:
            requests.Response — redirect responses are returned as-is.
        """
        logger.debug(f"POST {self._url(path)}")
        response = self.session.post(self._url(path), allow_redirects=False, **kwargs)
        self._log_response(response)
        return response

    def put(self, path: str, **kwargs) -> requests.Response:
        """
        Send a PUT request to base_url + path.

        Args:
            path: Relative endpoint path
            **kwargs: Passed directly to requests.Session.put

        Returns:
            requests.Response — redirect responses are returned as-is.
        """
        logger.debug(f"PUT {self._url(path)}")
        response = self.session.put(self._url(path), allow_redirects=False, **kwargs)
        self._log_response(response)
        return response

    def delete(self, path: str, **kwargs) -> requests.Response:
        """
        Send a DELETE request to base_url + path.

        Args:
            path: Relative endpoint path
            **kwargs: Passed directly to requests.Session.delete

        Returns:
            requests.Response — redirect responses are returned as-is.
        """
        logger.debug(f"DELETE {self._url(path)}")
        response = self.session.delete(self._url(path), allow_redirects=False, **kwargs)
        self._log_response(response)
        return response

    def close(self) -> None:
        """Close the underlying session and release connections."""
        self.session.close()
        logger.debug("APIClient session closed")
