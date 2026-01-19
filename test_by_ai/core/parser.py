from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class Endpoint:
    path: str
    method: str
    summary: str
    operation_id: str
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]]
    responses: Dict[str, Any]

class OpenAPIParser:
    def __init__(self, spec: dict):
        self.spec = spec
        self.base_path = spec.get('servers', [{'url': '/'}])[0].get('url', '/')
        if not self.base_path.startswith('http'):
             # If server url is relative or just path
            pass

    def get_endpoints(self) -> List[Endpoint]:
        endpoints = []
        paths = self.spec.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                    continue
                
                endpoints.append(Endpoint(
                    path=path,
                    method=method.upper(),
                    summary=details.get('summary', ''),
                    operation_id=details.get('operationId', ''),
                    parameters=details.get('parameters', []),
                    request_body=details.get('requestBody'),
                    responses=details.get('responses', {})
                ))
        return endpoints

    def get_server_url(self) -> str:
        """Simple extraction of first server URL or empty string"""
        servers = self.spec.get('servers', [])
        if servers:
            return servers[0].get('url', '')
        return ''
