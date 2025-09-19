import os 
import requests
from dotenv import load_dotenv

load_dotenv()

url_pdv_diario = "https://api.tiny.com.br/api2/pedidos.pesquisa.php"
url_pdv = "https://api.tiny.com.br/api2/pedido.obter.php"
TOKEN_API_TINY = os.getenv("TOKEN_API_TINY")


def obter_pdv_diario(data, formato="JSON"):
    """
    Função para retornar todos os pedidos de venda
    detalhados na data selecionada.
    
    """
    payload = {
        "token": TOKEN_API_TINY,
        "dataInicial": data,
        "dataFinal": data, 
        "formato": formato
    }
    
    response = requests.post(url_pdv_diario, data=payload)
    data = response.json()
    
    retorno = data.get("retorno", {})
    if "pedidos" not in retorno:
        print(f"Nenhum pedido encontrado para a data {data}")
        return []
    
    pedidos = retorno["pedidos"]
    
    pedidos = data["retorno"]["pedidos"]
    return [p["pedido"]["id"] for p in pedidos]

def obter_detalhes_pdv(id_pedido, formato="JSON"):
    payload = {
        "token": TOKEN_API_TINY,
        "id": id_pedido,
        "formato": formato
    }
    
    response = requests.post(url_pdv, data=payload)
    data = response.json()
    
    pedido = data["retorno"]["pedido"]

    resumo = {
        "numero_pedido": pedido.get("numero"),
        "data_pedido": pedido.get("data_pedido"),
        "cliente": pedido["cliente"].get("nome"),
        "situacao": pedido.get("situacao"),
        "Forma de Pagamento": pedido.get("forma_pagamento"),
        "Total do Pedido": pedido.get("total_pedido")
    }
    
    return resumo

def pedidos_diarios(data):
    ids_pedidos = obter_pdv_diario(data)
    if not ids_pedidos:  # lista vazia
        return []
    
    resultados = [obter_detalhes_pdv(pid) for pid in ids_pedidos]
    return resultados
    
    
if __name__ == "__main__":
    data = "08/09/2025"
    pdv_diarios = pedidos_diarios(data)
    
    print(pdv_diarios)