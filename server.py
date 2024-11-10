from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class GSIServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            if 'map' in data:
                clock_time = data['map'].get('clock_time', 0)
                print(f"Current game clock time: {clock_time}")
        except json.JSONDecodeError:
            print("Error decoding JSON data")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    server_address = ('localhost', 3030)
    httpd = HTTPServer(server_address, GSIServer)
    print("Starting GSI Server...")
    print("Waiting for Dota 2 data...")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()
        input("\nPress Enter to close...")

if __name__ == '__main__':
    run_server()