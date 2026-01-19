from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        elif self.path == '/users':
            self.send_response(200)
            self.header = ('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'[{"id": 1, "name": "Alice"}]')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/users':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            
            # Simple validation default
            if not body:
                self.send_response(400) # Bad Request
                self.end_headers()
                return
                
            try:
                data = json.loads(body)
                # Negative test check: if body empty or invalid?
                # Actually, our negative suite sends empty body.
                # So we expect 400 here if empty JSON or bad JSON.
                self.send_response(201)
                self.end_headers()
                self.wfile.write(b'{"id": 2}')
            except:
                self.send_response(400)
                self.end_headers()

def run_server():
    server = HTTPServer(('localhost', 8080), MockHandler)
    server.serve_forever()

if __name__ == '__main__':
    run_server()
