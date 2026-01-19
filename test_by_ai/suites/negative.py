from typing import List
from test_by_ai.core.results import TestResult, TestStatus, SuiteSummary
from test_by_ai.core.parser import Endpoint
from test_by_ai.core.http_client import APIClient
from test_by_ai.utils.common import simple_path_replace
from test_by_ai.suites.smoke import BaseSuite
import time

class NegativeSuite(BaseSuite):
    def __init__(self, client: APIClient, endpoints: List[Endpoint]):
        super().__init__(client, endpoints)
        self.name = "negative"

    async def run(self) -> SuiteSummary:
        summary = SuiteSummary(suite_name=self.name)
        
        for endpoint in self.endpoints:
            # Negative test: Send invalid requests.
            # 1. Empty body when body required
            # 2. Invalid types (not implemented heavily here to keep it simple/fast)
            
            path = simple_path_replace(endpoint.path)
            
            has_body = bool(endpoint.request_body)
            
            scenarios = []
            if has_body:
                scenarios.append(("empty_body", {}))
                scenarios.append(("invalid_types", {"foo": 123})) # Generic invalid payload

            if not scenarios:
                # If no body, maybe missing required params? 
                # For now simplify: if no body, we might skip negative test or try random unknown query param
                continue

            for case_name, payload in scenarios:
                start_time = time.time()
                try:
                    response = await self.client.request(
                        endpoint.method, 
                        path, 
                        json=payload
                    )
                    duration = (time.time() - start_time) * 1000
                    
                    # Expecting 4xx
                    # 5xx is FAIL
                    # 2xx is FAIL (should have rejected)
                    
                    code = response.status_code
                    status = TestStatus.PASS
                    error_msg = None
                    
                    if 500 <= code < 600:
                        status = TestStatus.FAIL
                        error_msg = f"Server Error {code} on negative test"
                    elif 200 <= code < 300:
                        status = TestStatus.FAIL
                        error_msg = f"Unexpected Success {code} on negative test"
                        
                    result = TestResult(
                        suite=self.name,
                        method=endpoint.method,
                        path=path,
                        status=status,
                        status_code=code,
                        duration_ms=duration,
                        error_message=f"[{case_name}] {error_msg}" if error_msg else None,
                        request_data=payload
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
