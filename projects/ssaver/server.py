import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from datetime import datetime

from terminal_grid_screensaver import GridScreensaver

class ContentHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/content':
            self._set_headers()
            # Generate dynamic content
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html = screensaver.run_once_html()
            content = f"""
            <div class="content">
                {html}
                <p>Current server time: {current_time}</p>
                <p>Server has been running for {time.time() - start_time:.2f} seconds.</p>
            </div>
            """
            response = {"html": content}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    global start_time
    start_time = time.time()
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, ContentHandler)
    print(f"Starting server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simple HTTP server that serves dynamic HTML content')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    args = parser.parse_args()

    screensaver = GridScreensaver()
    
    run_server(args.port)
