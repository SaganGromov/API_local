from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from gtts import gTTS
import json
import base64
import subprocess
import os

class APIHandler(BaseHTTPRequestHandler):
    USERNAME = 'user'
    PASSWORD = 'pass'

    def do_HEAD(self):
        self._authenticate()

    def do_GET(self):
        if not self._authenticate():
            return

        # Define main API route to run scripts
        if self.path.startswith('/api/run-script'):
            query_components = parse_qs(urlparse(self.path).query)
            script_name = query_components.get("script", [None])[0]

            # Define script paths
            script_paths = {
                "script1": "path/to/script1.sh",
                "script2": "path/to/script2.sh",
                "script3": "path/to/script3.sh"
            }

            if script_name in script_paths:
                result = self.run_script(script_paths[script_name])
                self.send_response(200 if result['status'] == 'success' else 500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Invalid script name"}).encode())

        # New endpoint to convert text to speech and play audio
        elif self.path.startswith('/api/speak'):
            query_components = parse_qs(urlparse(self.path).query)
            phrase = query_components.get("phrase", [None])[0]

            if phrase:
                result = self.generate_and_play_audio(phrase)
                self.send_response(200 if result['status'] == 'success' else 500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "No phrase provided"}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def run_script(self, script_path):
        try:
            output = subprocess.check_output(['bash', script_path], stderr=subprocess.STDOUT)
            return {'status': 'success', 'output': output.decode()}
        except subprocess.CalledProcessError as e:
            return {'status': 'error', 'output': e.output.decode()}

    def generate_and_play_audio(self, phrase):
        try:
            # Generate audio from phrase
            tts = gTTS(phrase, lang='en')
            audio_file = "phrase.mp3"
            tts.save(audio_file)

            # Play the generated audio file
            subprocess.run(['ffplay', '-nodisp', '-autoexit', audio_file])

            return {'status': 'success', 'message': f'Audio played for phrase: {phrase}'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _authenticate(self):
        if 'Authorization' in self.headers:
            auth_type, auth_data = self.headers['Authorization'].split(' ')
            if auth_type.lower() == 'basic':
                decoded_data = base64.b64decode(auth_data).decode()
                username, password = decoded_data.split(':')
                if username == self.USERNAME and password == self.PASSWORD:
                    return True

        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Access Restricted"')
        self.end_headers()
        self.wfile.write(b'Authentication Required')
        return False

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8000), APIHandler)
    print("API server running on port 8000")
    httpd.serve_forever()
