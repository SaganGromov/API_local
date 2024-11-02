from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from gtts import gTTS
import json
import base64
import time
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

        # Determine the endpoint
        if self.path == '/api/speak':
            self.handle_speak_request()
        elif self.path == '/api/alarm':
            self.handle_alarm_request()
        elif self.path == '/api/disable_alarms':
            self.handle_disable_alarms()
        else:
            # Invalid endpoint
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

    def handle_disable_alarms(self):
        # Stop all sleep and ffplay processes (alarms)
        subprocess.run("killall sleep", shell=True)  # Stops delayed alarms
        subprocess.run("killall ffplay", shell=True)  # Stops currently playing alarms

        # Respond to indicate success
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "message": "All alarms disabled"}).encode())

    def format_datetime_pt(self, now):
        formatted_time = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        return f"{formatted_time}".replace(":", " e ")

    def handle_speak_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        morse = data.get("morse", False)
        loop = data.get("loop", False)
        phrase = data.get("phrase")
        lang = data.get("lang", "pt")
        pararAlarme = data.get("parar")

        if loop:
            response_messages = []
            for i in range(1, 4):
                now = datetime.now()
                if int(self.format_datetime_pt(now)[:2]) <= 12:
                    sufixo = " da manhã"
                elif 12 < int(self.format_datetime_pt(now)[:2]) <= 17:
                    sufixo = " da tarde"
                else:
                    sufixo = " da noite"

                loop_phrase = f"Atualização realizada com sucesso às {self.format_datetime_pt(now)}" + sufixo
                time.sleep(5)
                result = self.generate_and_play_audio(loop_phrase, lang)
                response_messages.append(result)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_messages).encode())
        elif pararAlarme:
            subprocess.run("killall ffplay", shell=True)
            self.generate_and_play_audio("Alarme desativado com sucesso.", "pt")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "sucesso", "message": "alarme desativado!"}).encode())
        elif morse:
            message = data.get("message")
            subprocess.run('./script.sh ' + f'"{message}"', shell=True, capture_output=True, text=True)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            result = {'status': 'success', 'message': f'Código morse reproduzido: {message}'}
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
        elif phrase:
            result = self.generate_and_play_audio(phrase, lang)
            self.send_response(200 if result['status'] == 'success' else 500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "No phrase provided"}).encode())

    def format_alarm_time_to_pt(self, alarm_time):
        try:
            hour, minute = map(int, alarm_time.split('_'))
            alarm_dt = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            day_part = "da manhã" if hour < 12 else "da tarde" if hour < 18 else "da noite"
            time_str = alarm_dt.strftime(f"%H horas e %M minutos {day_part}")
            return time_str
        except ValueError:
            return "Formato de hora inválido"

    def handle_alarm_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if data.get("alarm") and "time" in data:
            alarm_time = data["time"]
            try:
                alarm_hour, alarm_minute = map(int, alarm_time.split('_'))
                now = datetime.now()
                alarm_datetime = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

                if alarm_datetime < now:
                    alarm_datetime += timedelta(days=1)

                delay = (alarm_datetime - now).total_seconds()
                subprocess.run(f"bash -c 'sleep {int(delay)}; ffplay -nodisp -autoexit -loop 0 mixkit-retro-game-emergency-alarm-1000.wav' &", shell=True)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.generate_and_play_audio(f"Alarme criado com sucesso para {self.format_alarm_time_to_pt(alarm_time)}! Bons sonhos.", "pt")
                self.wfile.write(json.dumps({"status": "success", "message": f"Alarm set for {alarm_time}"}).encode())
            except ValueError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Invalid time format"}).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Alarm flag or time missing"}).encode())

    def generate_and_play_audio(self, phrase, lang):
        try:
            tts = gTTS(phrase, lang=lang)
            audio_file = f"phrase_{phrase}.mp3"
            tts.save(audio_file)

            subprocess.run(['ffplay', '-nodisp', '-autoexit', audio_file])

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
