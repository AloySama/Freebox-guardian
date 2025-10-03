import hashlib
from dataclasses import dataclass
import json
import os
import requests
import hmac

from decorators.retry_on_403 import retry_on_403

CONFIG_FILE = "freebox_config.json"
HOST = "http://mafreebox.freebox.fr"
VERSION = "v15"

app_token_file = "app_token.txt"


@dataclass
class Freebox:
    mode: str = None
    app_id: str = None
    app_name: str = None
    app_version: str = None
    device_name: str = None
    app_token: str = None
    track_id: int = None
    _session_token: str = None

    def __post_init__(self):
        self.load_config()
        if self.mode == "build":
            self.create_app()
        elif self.mode == "token":
            self.login()

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
            self.track_id = data["track_id"]
            return None

    def create_app(self):
        print(f"[DEBUG] Creating app: {self.app_name} ({self.app_id})")

        r = requests.post(
            f"{HOST}/api/{VERSION}/login/authorize",
            json={
                "app_id": self.app_id,
                "app_name": self.app_name,
                "app_version": self.app_version,
                "device_name": self.device_name,
            }
        )

        self.app_token = r.json()["result"]["app_token"]
        self.track_id = r.json()["result"]["track_id"]

        self.authorize()
        self.mode = "token"
        self.save_config()


    def authorize(self):
        print("[DEBUG] Authorizing...")

        r = requests.get(f"{HOST}/api/{VERSION}/login/authorize/{self.track_id}")
        status = r.json()["result"]["status"]
        if status == "pending":
            print("[DEBUG] Authorization pending")

    def is_authorized(self):
        r = requests.get(f"{HOST}/api/{VERSION}/login/authorize/{self.track_id}")

        return "granted" == r.json()["result"]["status"]

    def login(self):
        print("[DEBUG] Logging in...")
        if not self.is_authorized():
            print("[ERROR] Authorization failed.")
            return

        r = requests.get(f"{HOST}/api/{VERSION}/login/")

        challenge: str = r.json()["result"]["challenge"]
        password = hmac.new(self.app_token.encode(), challenge.encode(), hashlib.sha1).hexdigest()


        r = requests.post(
            f"{HOST}/api/{VERSION}/login/session",
            json={
                "app_id": self.app_id,
                "password": password,
            }
        )

        success = r.json()["success"]

        if not success:
            return

        self._session_token = r.json()["result"]["session_token"]

    def logout(self):
        print("[DEBUG] Logging out...")

    @retry_on_403(max_retries=3)
    def get_connection_info(self):
        pass






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
