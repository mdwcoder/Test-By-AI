import asyncio
from typing import List
from test_by_ai.core.results import TestResult, TestStatus, SuiteSummary
from test_by_ai.core.parser import Endpoint
from test_by_ai.core.http_client import APIClient
import time

class BaseSuite:
    def __init__(self, client: APIClient, endpoints: List[Endpoint]):
        self.client = client
        self.endpoints = endpoints
        self.name = "base"

    async def run(self) -> SuiteSummary:
        summary = SuiteSummary(suite_name=self.name)
        return summary

class SmokeSuite(BaseSuite):
    def __init__(self, client: APIClient, endpoints: List[Endpoint]):
        super().__init__(client, endpoints)
        self.name = "smoke"

    async def run(self) -> SuiteSummary:
        summary = SuiteSummary(suite_name=self.name)
        
        # Filter for GET requests for smoke tests usually, 
        # or minimal viable request for others.
        # Requirement: "Ejecuta una request mínima válida por endpoint"
        
        for endpoint in self.endpoints:
            # We prioritize GET for smoke as they are usually side-effect free
            # For POST/PUT/DELETE we might skip or try without body if allowed,
            # but usually Smoke = Health checks.
            # User said: "Ejecuta una request mínima válida por endpoint" implies all endpoints.
            # But sending POST without body might be invalid.
            # We will try best effort.
            
            start_time = time.time()
            try:
                # Basic strategy: If GET, call it. If other, check if no body required.
                # Construct path params if any (using defaults or placeholders)
                # For now, strict smoke test often implies just checking if endpoint reachable.
                # We will replace path parameters with '1' or 'test' dummy values.
                
                path = endpoint.path
                if "{" in path:
                     # Simple path param replacement
                     # In a real tool this needs better inference
                     import re
                     path = re.sub(r'\{.*?\}', '1', path)

                # Skip methods that usually require body for smoke if we can't generate it easily?
                # or just send empty and expect proper error handling?
                # Smoke definition: "Valida que responde, que no devuelve 5xx".
                
                response = await self.client.request(endpoint.method, path)
                duration = (time.time() - start_time) * 1000
                
                status = TestStatus.PASS
                if response.status_code >= 500:
                    status = TestStatus.FAIL
                # We don't fail on 4xx for smoke checks on complex endpoints without data
                
                result = TestResult(
                    suite=self.name,
                    method=endpoint.method,
                    path=path,
                    status=status,
                    status_code=response.status_code,
                    duration_ms=duration,
                    response_data=None # Don't store full response to save memory
                )
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                result = TestResult(
                    suite=self.name,
                    method=endpoint.method,
                    path=endpoint.path,
                    status=TestStatus.ERROR,
                    duration_ms=duration,
                    error_message=str(e)
                )
            
            summary.add_result(result)
            
        return summary
