from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from gtts import gTTS
import json
import base64
import subprocess
import os
from datetime import datetime, timedelta

class APIHandler(BaseHTTPRequestHandler):
    USERNAME = 'user'
    PASSWORD = 'pass'

    def do_HEAD(self):
        self._authenticate()

    def do_POST(self):
        if not self._authenticate():
            return

        # Process the POST request for the `/api/speak` endpoint
        if self.path == '/api/speak':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            morse=data.get("morse", False)
            loop = data.get("loop", False)  # Check if loop is requested
            phrase = data.get("phrase")
            lang = data.get("lang", "pt")  # Default to Portuguese if no language is specified

            # Handle loop requests
            if loop:
                response_messages = []
                for i in range(1, 6):  # Adjust range for desired repetitions
                    loop_phrase = f"Botafogo {i}, Peñarol 0"
                    result = self.generate_and_play_audio(loop_phrase, lang)
                    response_messages.append(result)

                # Send combined results for loop
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_messages).encode())
            elif morse:
                message=data.get("message")
                subprocess.run('./script.sh ' + f'"{message}"', shell=True, capture_output=True, text=True)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                result = {'status': 'success', 'message': f'Código morse reproduzido: {message}'}
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            elif phrase:
                # Handle single phrase request
                result = self.generate_and_play_audio(phrase, lang)
                self.send_response(200 if result['status'] == 'success' else 500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            elif self.path == '/api/alarm':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                if data.get("alarm") and "time" in data:
                    alarm_time = data["time"]
                    try:
                        # Parse HH_MM format
                        alarm_hour, alarm_minute = map(int, alarm_time.split('_'))
                        now = datetime.now()
                        alarm_datetime = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

                        # If the time has already passed today, set it for tomorrow
                        if alarm_datetime < now:
                            alarm_datetime += timedelta(days=1)

                        # Calculate the delay in seconds until the alarm time
                        delay = (alarm_datetime - now).total_seconds()

                        # Schedule ffplay to run at the specified time
                        subprocess.Popen(["sleep", str(delay), "&&", "ffplay", "-nodisp", "-autoexit", 
                                        "mixkit-retro-game-emergency-alarm-1000.wav"], shell=True)

                        # Send response
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.generate_and_play_audio(f"Alarme criado para {alarm_time} com sucesso! Bons sonhos.")
                        self.wfile.write(json.dumps({"status": "success", "message": "Alarm set for " + alarm_time}).encode())
                    except ValueError:
                        # Invalid time format provided
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "error", "message": "Invalid time format"}).encode())
                else:
                    # Alarm or time missing in the request
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "Alarm flag or time missing"}).encode())
            else:
                # No phrase provided
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "No phrase provided"}).encode())
        
        else:
            # Invalid endpoint
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def run_script(self, script_path):
        try:
            output = subprocess.check_output(['bash', script_path], stderr=subprocess.STDOUT)
            return {'status': 'success', 'output': output.decode()}
        except subprocess.CalledProcessError as e:
            return {'status': 'error', 'output': e.output.decode()}

    def generate_and_play_audio(self, phrase, lang):
        try:
            # Generate audio from phrase in the specified language
            tts = gTTS(phrase, lang=lang)
            audio_file = f"phrase_{phrase}.mp3"
            tts.save(audio_file)

            # Play the generated audio file
            subprocess.run(['ffplay', '-nodisp', '-autoexit', audio_file])

            # Delete the audio file after playing it
            if os.path.exists(audio_file):
                os.remove(audio_file)

            return {'status': 'success', 'message': f'Audio played for phrase: {phrase} in language: {lang}'}
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
    httpd = HTTPServer(('0.0.0.0', 8000), APIHandler)
    print("API server running on port 8000")
    httpd.serve_forever()
