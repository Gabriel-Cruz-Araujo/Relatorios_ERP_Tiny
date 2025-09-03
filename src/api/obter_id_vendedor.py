import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.tiny.com.br/api2/vendedores.pesquisa.php"
TOKEN = os.getenv("TOKEN_API_TINY")


payload = {
    "token": TOKEN,
    "formato": "JSON"
}

response = requests.post(API_URL, data=payload)
data = response.json()

print(data)