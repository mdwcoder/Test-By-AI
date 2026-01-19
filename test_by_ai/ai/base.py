from abc import ABC, abstractmethod
from typing import Optional
from test_by_ai.core.results import GlobalRunResult

class AIProvider(ABC):
    @abstractmethod
    async def analyze(self, result: GlobalRunResult) -> str:
        """Analyze the test results and return insights."""
        pass
