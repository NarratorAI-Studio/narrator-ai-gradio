"""HTTP client for Narrator AI API — extracted from narrator-ai-cli, no CLI dependencies."""

import json as _json
import os
from typing import Any, Optional, Iterator

import httpx
from httpx_sse import connect_sse

DEFAULT_SERVER = "https://openapi.jieshuo.cn"
SUCCESS = 10000


class NarratorAPIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class NarratorClient:
    def __init__(self, server: Optional[str] = None, app_key: Optional[str] = None, timeout: int = 60):
        self.server = server or os.environ.get("NARRATOR_SERVER", DEFAULT_SERVER)
        self.app_key = app_key or os.environ.get("NARRATOR_APP_KEY", "")
        self.timeout = timeout
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(timeout=self.timeout, headers={"app-key": self.app_key})
        return self._client

    def _url(self, path: str) -> str:
        return f"{self.server}{path}"

    def _handle(self, resp: httpx.Response) -> dict:
        resp.raise_for_status()
        data = resp.json()
        code = data.get("code", 0)
        if code != SUCCESS:
            raise NarratorAPIError(code, data.get("message", "Unknown error"))
        return data.get("data") or {}

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        return self._handle(self._get_client().get(self._url(path), params=params))

    def post(self, path: str, json: Optional[dict] = None) -> Any:
        return self._handle(self._get_client().post(self._url(path), json=json))

    def post_sse(self, path: str, json: Optional[dict] = None) -> Iterator[tuple[str, dict]]:
        headers = {"app-key": self.app_key, "Accept": "text/event-stream"}
        with httpx.Client(timeout=httpx.Timeout(self.timeout, read=300.0)) as c:
            with connect_sse(c, "POST", self._url(path), json=json, headers=headers) as sse:
                for event in sse.iter_sse():
                    try:
                        data = _json.loads(event.data) if event.data else {}
                    except _json.JSONDecodeError:
                        data = {"raw": event.data}
                    yield event.event, data

    def delete(self, path: str, params: Optional[dict] = None) -> Any:
        return self._handle(self._get_client().delete(self._url(path), params=params))

    def upload_file(self, upload_url: str, file_path: str, content_type: str):
        with open(file_path, "rb") as f:
            httpx.Client(timeout=300).put(upload_url, content=f, headers={"Content-Type": content_type})

    def close(self):
        if self._client and not self._client.is_closed:
            self._client.close()
