import os
import httpx
import json
from test_by_ai.ai.base import AIProvider
from test_by_ai.core.results import GlobalRunResult

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

    async def analyze(self, result: GlobalRunResult) -> str:
        # Prepare prompt
        summary_dict = result.to_dict()
        # Simplify for context window if needed, but results are usually small-ish for this CLI scope
        
        prompt = f"""
Act as a Senior QA Engineer and Backend Developer.
Analyze the following automated API test results.
Focus on:
1. Probable causes for failures (Status verification, Schema validation, etc).
2. Patterns in errors (e.g. all POSTs failing, or specific 500 errors).
3. Suggestions for fixes.
4. Detect bad practices if any (e.g. 200 OK but error body).

Results JSON:
{json.dumps(summary_dict, indent=2)}

Provide a concise, professional summary in Markdown.
"""
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.url, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    return "Error parsing Gemini response."
            except Exception as e:
                return f"Failed to call Gemini API: {e}"
