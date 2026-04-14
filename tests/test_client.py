"""Tests for the NarratorClient HTTP client."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from client import DEFAULT_SERVER, NarratorAPIError, NarratorClient


class TestNarratorAPIError:
    def test_has_code_and_message(self) -> None:
        err = NarratorAPIError(20001, "Something went wrong")
        assert err.code == 20001
        assert err.message == "Something went wrong"

    def test_str_representation(self) -> None:
        err = NarratorAPIError(20001, "fail")
        assert "[20001]" in str(err)
        assert "fail" in str(err)


class TestNarratorClientInit:
    def test_defaults(self) -> None:
        client = NarratorClient()
        assert client.server == DEFAULT_SERVER
        assert client.timeout == 60

    def test_custom_values(self) -> None:
        client = NarratorClient(server="https://example.com", app_key="abc123", timeout=30)
        assert client.server == "https://example.com"
        assert client.app_key == "abc123"
        assert client.timeout == 30


class TestUrlConstruction:
    def test_url(self) -> None:
        client = NarratorClient(server="https://api.test.com")
        assert client._url("/v2/foo") == "https://api.test.com/v2/foo"


class TestHandle:
    def test_success_response(self) -> None:
        client = NarratorClient()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"code": 10000, "data": {"foo": "bar"}}
        mock_resp.raise_for_status = MagicMock()

        result = client._handle(mock_resp)
        assert result == {"foo": "bar"}

    def test_error_response_raises(self) -> None:
        client = NarratorClient()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"code": 20001, "message": "Bad request"}
        mock_resp.raise_for_status = MagicMock()

        with pytest.raises(NarratorAPIError) as exc_info:
            client._handle(mock_resp)
        assert exc_info.value.code == 20001
        assert exc_info.value.message == "Bad request"

    def test_http_error_raises(self) -> None:
        import httpx

        client = NarratorClient()
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error",
            request=MagicMock(),
            response=MagicMock(status_code=500),
        )

        with pytest.raises(httpx.HTTPStatusError):
            client._handle(mock_resp)


class TestGetAndPost:
    def test_get_calls_client_correctly(self) -> None:
        client = NarratorClient(server="https://api.test.com", app_key="key123")

        mock_httpx_client = MagicMock()
        mock_httpx_client.is_closed = False
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 10000, "data": {"items": []}}
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.get.return_value = mock_response

        client._client = mock_httpx_client

        result = client.get("/v2/tasks", params={"page": 1})
        mock_httpx_client.get.assert_called_once_with("https://api.test.com/v2/tasks", params={"page": 1})
        assert result == {"items": []}

    def test_post_calls_client_correctly(self) -> None:
        client = NarratorClient(server="https://api.test.com", app_key="key123")

        mock_httpx_client = MagicMock()
        mock_httpx_client.is_closed = False
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 10000, "data": {"task_id": "abc"}}
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client._client = mock_httpx_client

        result = client.post("/v2/task/create", json={"name": "test"})
        mock_httpx_client.post.assert_called_once_with("https://api.test.com/v2/task/create", json={"name": "test"})
        assert result == {"task_id": "abc"}


class TestPostNoAuth:
    def test_post_no_auth_does_not_use_app_key(self) -> None:
        client = NarratorClient(server="https://api.test.com", app_key="should-not-appear")

        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 10000, "data": {"token": "xyz"}}
        mock_response.raise_for_status = MagicMock()

        with patch("client.httpx.Client") as mock_client_cls:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_client_cls.return_value = mock_instance

            result = client.post_no_auth("/v1/users/sign_in", json={"username": "u", "password": "p"})
            mock_instance.post.assert_called_once_with(
                "https://api.test.com/v1/users/sign_in", json={"username": "u", "password": "p"}
            )
            assert result == {"token": "xyz"}
