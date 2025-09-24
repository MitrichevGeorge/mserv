import requests
import socket
import threading
import time
import subprocess


SERVER_URL = "https://geomit22.pythonanywhere.com"


class Client:
    def __init__(self, server_url):
        self.server_url = server_url
        self.hostname = socket.gethostname()
        self.ip = self._get_local_ip()
        self.ssid = self._get_ssid()
        self.info = self.hostname
        self._stop_event = threading.Event()
        self._thread = None

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _get_ssid(self):
        try:
            result = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
            if result:
                return result
        except Exception:
            pass

        try:
            result = subprocess.check_output(
                ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], text=True
            )
            for line in result.splitlines():
                if line.startswith("yes:"):
                    return line.split(":", 1)[1]
        except Exception:
            pass

        return "Unknown"

    def register(self):
        try:
            r = requests.post(f"{self.server_url}/register", json={
                "ip": self.ip,
                "ssid": self.ssid,
                "info": self.info
            }, timeout=5)
            print("Register:", r.json())
        except Exception as e:
            print("Register failed:", e)

    def _ping_loop(self):
        while not self._stop_event.is_set():
            try:
                r = requests.post(f"{self.server_url}/ping", json={"ip": self.ip}, timeout=5)
                print("Ping:", r.json())
            except Exception as e:
                print("Ping failed:", e)
            self._stop_event.wait(10)

    def run(self):
        """Запустить регистрацию и фоновый поток пинга"""
        self.register()
        self._thread = threading.Thread(target=self._ping_loop, daemon=True)
        self._thread.start()
        print("Client started in background.")

    def stop(self):
        """Остановить фоновый поток"""
        self._stop_event.set()
        if self._thread:
            self._thread.join()


if __name__ == "__main__":
    client = Client(SERVER_URL)
    client.run()
    time.sleep(30)
