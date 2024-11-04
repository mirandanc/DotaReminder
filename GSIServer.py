from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class GSIServer(BaseHTTPRequestHandler):
    clock_time = 0  # Class variable to store clock_time
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        gsi_data = json.loads(body)
        
        try:
            GSIServer.clock_time = gsi_data['map']['clock_time']
            print(f"Current clock time: {GSIServer.clock_time}")
        except KeyError:
            print("Clock time not found in GSI data")

        self.send_response(200)
        self.end_headers()

def start_server():
    server = HTTPServer(('localhost', 3000), GSIServer)
    print("GSI Server running on port 3000")
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

def get_clock_time():
    return GSIServer.clock_time