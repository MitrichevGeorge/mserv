import requests, socket, subprocess, uuid, os, threading, time

SERVER_URL = "https://geomit22.pythonanywhere.com"

ID_FILE = "id"

def get_or_create_id():
    if not os.path.exists(ID_FILE):
        return None
    with open(ID_FILE) as f:
        return f.read().strip()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def get_ssid():
    try:
        return subprocess.check_output(["iwgetid", "-r"], text=True).strip()
    except:
        try:
            out = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], text=True)
            for line in out.splitlines():
                active, ssid = line.split(":")
                if active == "yes":
                    return ssid
        except:
            return "Unknown"
    return "Unknown"

class Client:
    def __init__(self):
        self.id = get_or_create_id()
        if not self.id:
            raise RuntimeError("No id file!")
        self.stop = False

    def register(self):
        data = {"id": self.id, "ip": get_ip(), "ssid": get_ssid()}
        requests.post(f"{SERVER_URL}/register", json=data)

    def ping(self):
        data = {"id": self.id, "ip": get_ip(), "ssid": get_ssid()}
        requests.post(f"{SERVER_URL}/ping", json=data)

    def run(self):
        self.register()
        def loop():
            while not self.stop:
                try:
                    self.ping()
                except Exception as e:
                    print("Ping error:", e)
                time.sleep(10)
        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    c = Client()
    c.run()
    print("Client running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        c.stop = True
