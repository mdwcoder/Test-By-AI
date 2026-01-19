import asyncio
from typing import List, Optional
from test_by_ai.core.loader import load_spec
from test_by_ai.core.parser import OpenAPIParser
from test_by_ai.core.http_client import APIClient
from test_by_ai.core.results import GlobalRunResult
from test_by_ai.suites.smoke import SmokeSuite
from test_by_ai.suites.contract import ContractSuite
from test_by_ai.suites.negative import NegativeSuite
from test_by_ai.ai.base import AIProvider

class TestRunner:
    def __init__(self, openapi_path: str, base_url: Optional[str] = None):
        self.openapi_path = openapi_path
        self.base_url = base_url
        self.spec = None
        self.endpoints = []
        
    def load(self):
        self.spec = load_spec(self.openapi_path)
        parser = OpenAPIParser(self.spec)
        self.endpoints = parser.get_endpoints()
        if not self.base_url:
            self.base_url = parser.get_server_url()
        
        if not self.base_url:
            raise ValueError("Base URL not found in spec and not provided explicitly.")

    async def run(self, suites: List[str], ai_provider: Optional[AIProvider] = None) -> GlobalRunResult:
        if not self.spec:
            self.load()
            
        results = GlobalRunResult()
        
        async with APIClient(self.base_url) as client:
            if 'smoke' in suites or 'all' in suites:
                suite = SmokeSuite(client, self.endpoints)
                results.suites.append(await suite.run())
                
            if 'contract' in suites or 'all' in suites:
                suite = ContractSuite(client, self.endpoints)
                results.suites.append(await suite.run())
                
            if 'negative' in suites or 'all' in suites:
                suite = NegativeSuite(client, self.endpoints)
                results.suites.append(await suite.run())

        if ai_provider and results.has_failures:
            # Only analyze if there are interesting things (failures), or maybe always if user asked?
            # User said: "La IA SOLO: Analiza resultados ya obtenidos... Explica causas probables de errores"
            # It implies mostly useful when there are errors, but could also critique success (smells).
            # We'll run it always if requested, but prompt might vary. Default prompt handles both.
            results.ai_analysis = await ai_provider.analyze(results)
            
        return results
