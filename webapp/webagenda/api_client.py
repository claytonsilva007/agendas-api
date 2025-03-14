import requests
import datetime
import pytz
from django.conf import settings

# API_URL = "http://api:8000/api/agenda/"
# API_TOKEN_URL = "http://api:8000/api/token"

API_URL = "http://127.0.0.1/api/agenda/"
API_TOKEN_URL = "http://127.0.0.1/api/token/"

class APIClient:
    _token = None  # Cache do token para reuso
    _token_expiration = None

    @classmethod
    def _atualizar_token(cls):
        """Obtém um novo token JWT e armazena para reutilização."""
        response = requests.post(API_TOKEN_URL, data={"username": "admin", "password": "admin123"})
        
        if response.status_code == 200:
            token_data = response.json()
            cls._token = token_data.get("access")
            cls._token_expiration = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=token_data.get("expires_in", 3600))
        else:
            raise Exception("Falha ao obter token JWT")

    @classmethod
    def _get_token(cls):
        """Retorna um token válido, atualizando se necessário."""
        if cls._token is None or datetime.datetime.now(pytz.utc) >= cls._token_expiration:
            cls._atualizar_token()
        return cls._token

    @classmethod
    def _get_headers(cls):
        """Retorna os headers com o token de autenticação."""
        return {
            "Authorization": f"Bearer {cls._get_token()}",
            "Content-Type": "application/json"
        }

    @classmethod
    def get(cls, endpoint):
        """Realiza uma requisição GET autenticada."""
        headers = cls._get_headers()
        response = requests.get(f"{API_URL}{endpoint}", headers=headers)

        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    def post(cls, endpoint, data):
        """Realiza uma requisição POST autenticada."""
        headers = cls._get_headers()
        response = requests.post(f"{API_URL}{endpoint}", json=data, headers=headers)

        if response.status_code == 201:
            return response.json()
        return None

    @classmethod
    def put(cls, endpoint, data):
        """Realiza uma requisição PUT autenticada."""
        headers = cls._get_headers()
        response = requests.put(f"{API_URL}{endpoint}", json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    def delete(cls, endpoint):
        """Realiza uma requisição DELETE autenticada."""
        headers = cls._get_headers()
        response = requests.delete(f"{API_URL}{endpoint}", headers=headers)

        if response.status_code == 204:
            return True
        return False