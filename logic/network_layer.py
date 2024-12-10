import httpx


class NetworkLayer:
    BASE_URL = "http://localhost:5321"

    def __init__(self):
        self.token = None
        self.app_source = "staff"

    def set_token(self, token):
        self.token = token

    def get_headers(self):
        if not self.token:
            raise ValueError("Токен отсутствует")
        return {
            "Authorization": f"Bearer {self.token}",
            "X-App-Source": self.app_source
        }

    def get(self, endpoint, headers=None, params=None):
        try:
            response = httpx.get(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                params=params,
                timeout=10
            )
            return {"status": response.status_code, "data": response.json()} if response.status_code == 200 else {"status": response.status_code, "detail": response.json().get("detail", "Ошибка")}
        except httpx.RequestError as e:
            return {"status": 0, "detail": f"Ошибка подключения: {str(e)}"}

    def post(self, endpoint, headers=None, json=None, params=None):
        try:
            response = httpx.post(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                json=json,
                params=params,
                timeout=10
            )
            return {"status": response.status_code, "data": response.json()} if response.status_code == 200 else {"status": response.status_code, "detail": response.json().get("detail", "Ошибка")}
        except httpx.RequestError as e:
            return {"status": 0, "detail": f"Ошибка подключения: {str(e)}"}

    def put(self, endpoint, headers=None, json=None, params=None):
        """Выполняет PUT-запрос."""
        try:
            response = httpx.put(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                json=json,
                params=params,
                timeout=10
            )
            if response.status_code == 200:
                return {"status": 200, "data": response.json()}
            else:
                return {"status": response.status_code, "detail": response.json().get("detail", "Неизвестная ошибка")}
        except httpx.RequestError as e:
            return {"status": 0, "detail": f"Ошибка подключения: {str(e)}"}

    def delete(self, endpoint, headers=None):
        """Выполняет DELETE-запрос."""
        try:
            response = httpx.delete(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return {"status": 200, "data": response.json()}
            else:
                return {"status": response.status_code, "detail": response.json().get("detail", "Неизвестная ошибка")}
        except httpx.RequestError as e:
            return {"status": 0, "detail": f"Ошибка подключения: {str(e)}"}