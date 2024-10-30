from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import subprocess

class APIHandler(BaseHTTPRequestHandler):
    USERNAME = 'user'
    PASSWORD = 'pass'

    def do_HEAD(self):
        self._authenticate()

    def do_GET(self):
        if not self._authenticate():
            return

        if self.path == '/api/data':
            # Standard API response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'message': 'Hello, this is your API!',
                'status': 'success'
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/api/run-script':
            # Run the shell script
            result = self.run_script('s.sh')
            self.send_response(200 if result['status'] == 'success' else 500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        else:
            # 404 Not Found if endpoint doesn't exist
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def run_script(self, script_path):
        try:
            # Run the shell script and capture output
            output = subprocess.check_output(['bash', script_path], stderr=subprocess.STDOUT)
            return {'status': 'success', 'output': output.decode()}
        except subprocess.CalledProcessError as e:
            return {'status': 'error', 'output': e.output.decode()}

    def _authenticate(self):
        if 'Authorization' in self.headers:
            auth_type, auth_data = self.headers['Authorization'].split(' ')
            if auth_type.lower() == 'basic':
                decoded_data = base64.b64decode(auth_data).decode()
                username, password = decoded_data.split(':')
                if username == self.USERNAME and password == self.PASSWORD:
                    return True

        # Authentication failure response
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Access Restricted"')
        self.end_headers()
        self.wfile.write(b'Authentication Required')
        return False

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8000), APIHandler)
    print("API server running on port 8000")
    httpd.serve_forever()
