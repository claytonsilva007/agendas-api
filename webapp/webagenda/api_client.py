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
    def get(cls, endpoint):
        """Realiza uma requisição GET autenticada."""
        headers = {"Authorization": f"Bearer {cls._get_token()}"}
        response = requests.get(f"{API_URL}{endpoint}", headers=headers)

        if response.status_code == 200:
            return response.json()
        return None
