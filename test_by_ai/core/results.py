from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict
from enum import Enum

class TestStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"

@dataclass
class TestResult:
    suite: str
    method: str
    path: str
    status: TestStatus
    status_code: Optional[int] = None
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    request_data: Optional[Dict[str, Any]] = None
    response_data: Optional[Any] = None
    
    def __str__(self):
        return f"[{self.status.value}] {self.method} {self.path} ({self.status_code})"

@dataclass
class SuiteSummary:
    suite_name: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    results: List[TestResult] = field(default_factory=list)
    
    def add_result(self, result: TestResult):
        self.total += 1
        self.results.append(result)
        if result.status == TestStatus.PASS:
            self.passed += 1
        elif result.status == TestStatus.FAIL:
            self.failed += 1
        elif result.status == TestStatus.ERROR:
            self.errors += 1
        else:
            self.skipped += 1

@dataclass
class GlobalRunResult:
    suites: List[SuiteSummary] = field(default_factory=list)
    ai_analysis: Optional[str] = None
    
    @property
    def has_failures(self) -> bool:
        return any(s.failed > 0 or s.errors > 0 for s in self.suites)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": {
                "total": sum(s.total for s in self.suites),
                "passed": sum(s.passed for s in self.suites),
                "failed": sum(s.failed for s in self.suites),
                "errors": sum(s.errors for s in self.suites)
            },
            "suites": [
                {
                    "name": s.suite_name,
                    "results": [
                        {
                            "method": r.method,
                            "path": r.path,
                            "status": r.status.value,
                            "status_code": r.status_code,
                            "error": r.error_message
                        } for r in s.results if r.status != TestStatus.PASS
                    ]
                } for s in self.suites
            ],
            "ai_analysis": self.ai_analysis
        }
