import http.server
import socketserver
import json
import os

# Store the shared state
current_name = ""

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve files from the 'public' directory
        super().__init__(*args, directory="public", **kwargs)

    def do_GET(self):
        if self.path == '/api/name':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.end_headers()
            self.wfile.write(json.dumps({"name": current_name}).encode())
        else:
            # Super call handles serving static files
            super().do_GET()

    def do_POST(self):
        global current_name
        if self.path == '/api/name':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                if 'name' in data and isinstance(data['name'], str):
                    name = data['name'].strip()
                    if len(name) <= 100:
                        current_name = name
            except Exception:
                pass

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        else:
            self.send_error(404)

    def end_headers(self):
        # Basic CSP for security
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com;")
        super().end_headers()

PORT = int(os.environ.get('PORT', 8000))
# To allow access from other devices, run with HOST=0.0.0.0
HOST = os.environ.get('HOST', '127.0.0.1')

if __name__ == "__main__":
    with socketserver.ThreadingTCPServer((HOST, PORT), Handler) as httpd:
        print(f"Server listening on http://{HOST}:{PORT}")
        print("To allow connections from other machines, set environment variable HOST=0.0.0.0")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
