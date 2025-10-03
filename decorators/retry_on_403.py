from functools import wraps
import requests


def retry_on_403(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = func(self, *args, **kwargs)
                    # Si la fonction retourne un dict avec status_code 403
                    if isinstance(result, dict) and result.get("error_code") == 403:
                        print("[DEBUG] 403 detected, relogging...")
                        self.login()
                        continue
                    return result
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 403:
                        print("[DEBUG] 403 detected, relogging...")
                        self.login()
                        continue
                    raise  # autre erreur → remonte
            raise Exception(f"Max retries ({max_retries}) reached")
        return wrapper
    return decorator
