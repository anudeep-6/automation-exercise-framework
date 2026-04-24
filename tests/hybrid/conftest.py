"""
Hybrid test fixtures — tests/hybrid/conftest.py

Hybrid tests combine the UI and API layers in a single test.
Both the `page` fixture (Playwright) and `api_client` fixture (requests)
are inherited from the root conftest and tests/api/conftest respectively —
no re-declaration needed here.

This conftest is the extension point for any hybrid-specific fixtures,
e.g. a fixture that seeds data via the API and then navigates the UI
to verify the result.
"""
