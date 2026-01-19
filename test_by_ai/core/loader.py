import json
import httpx
import os
from urllib.parse import urlparse

def load_spec(path_or_url: str) -> dict:
    """Load OpenAPI spec from local file or URL."""
    parsed = urlparse(path_or_url)
    if parsed.scheme in ('http', 'https'):
        try:
            response = httpx.get(path_or_url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to load OpenAPI from URL: {e}")
    else:
        if not os.path.exists(path_or_url):
            raise FileNotFoundError(f"OpenAPI file not found: {path_or_url}")
        try:
            with open(path_or_url, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to read file: {e}")
