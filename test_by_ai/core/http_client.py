import httpx
import time
from typing import Any, Dict, Optional

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)

    async def close(self):
        await self.client.aclose()

    async def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}{path}"
        try:
            return await self.client.request(method, url, **kwargs)
        except httpx.RequestError as e:
            # Create a dummy response object or re-raise wrapped
            raise e

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
