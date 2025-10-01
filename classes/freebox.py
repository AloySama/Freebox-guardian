from dataclasses import dataclass
import json
import os

CONFIG_FILE = "freebox_config.json"


@dataclass
class Freebox:
    mode: str = None
    app_id: str = None
    app_name: str = None
    app_version: str = None
    device_name: str = None
    app_token: str = None

    @classmethod
    def from_config(cls):
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError("Config file not found.")
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return cls(**data)

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.__dict__, f, indent=2)

    def load_config(self):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            self.mode = data["mode"]
            self.app_id = data["app_id"]
            self.app_name = data["app_name"]
            self.app_version = data["app_version"]
            self.device_name = data["device_name"]
            self.app_token = data["app_token"]
            return None

    def create_app(self):
        print(f"[DEBUG] Creating app: {self.app_name} ({self.app_id})")

    def authorize(self):
        print("[DEBUG] Authorizing...")

    def login(self):
        print("[DEBUG] Logging in...")

    def get_session_token(self):
        print("[DEBUG] Getting session token...")

    def logout(self):
        print("[DEBUG] Logging out...")



'''
{
 session_token
}


GET /api/v4/connection/

GET /api/v4/connection/ftth/

GET /api/v4/system/

GET /api/v4/lan/browser/interfaces/ + GET /api/v4/lan/browser/{interface}

GET /api/v4/call/log/

GET /api/v4/wifi/
'''
