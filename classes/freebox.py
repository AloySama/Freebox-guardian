from dataclasses import dataclass


@dataclass
class Freebox:
    def create_app(self):
        pass

    def authorize(self):
        pass

    def login(self):
        pass

    def get_session_token(self):
        pass

    def logout(self):
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