import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

url_pdv_diario = "https://api.tiny.com.br/api2/pedidos.pesquisa.php"
url_pdv = "https://api.tiny.com.br/api2/pedido.obter.php"
TOKEN_API_TINY = os.getenv("TOKEN_API_TINY")


def obter_pdv_diario_mensal(data_inicial, data_final, formato="JSON"):
    """
    Retorna os IDs de pedidos no período informado.
    Retorna lista vazia se nenhum pedido for encontrado.
    """
    payload = {
        "token": TOKEN_API_TINY,
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "formato": formato
    }

    response = requests.post(url_pdv_diario, data=payload)
    data = response.json()

    retorno = data.get("retorno", {})
    if "pedidos" not in retorno or not retorno["pedidos"]:
        print(f"Nenhum pedido encontrado no período {data_inicial} até {data_final}")
        return []

    pedidos = retorno["pedidos"]
    return [p["pedido"]["id"] for p in pedidos]


def obter_detalhes_pdv_mensal(id_pedido, formato="JSON"):
    """
    Retorna os detalhes de um pedido específico em uma linha,
    concatenando todos os produtos em uma única célula.
    """
    payload = {
        "token": TOKEN_API_TINY,
        "id": id_pedido,
        "formato": formato
    }

    response = requests.post(url_pdv, data=payload)
    data = response.json()

    pedido = data.get("retorno", {}).get("pedido")
    if not pedido:
        print(f"Atenção: pedido {id_pedido} não encontrado ou retorno inválido")
        return None  # ignora pedidos inválidos

    produtos = [item["item"]["descricao"] for item in pedido.get("itens", [])]
    produtos_str = ", ".join(produtos)

    resumo = {
        "numero_pedido": pedido.get("numero"),
        "data_pedido": pedido.get("data_pedido"),
        "cliente": pedido["cliente"].get("nome"),
        "situacao": pedido.get("situacao"),
        "forma_pagamento": pedido.get("forma_pagamento"),
        "meio_pagamento": pedido.get("meio_pagamento"),
        "total_pedido": pedido.get("total_pedido"),
        "nome_vendedor": pedido.get("nome_vendedor"),
        "produtos": produtos_str
    }

    return resumo


def pedidos_diarios_mensal(data_inicial, data_final, formato="JSON", delay=2):
    """
    Retorna todos os pedidos do período em uma linha por pedido.
    Ignora pedidos inválidos e continua mesmo se não houver vendas.
    delay: tempo em segundos entre chamadas para não sobrecarregar a API
    """
    ids_pedidos = obter_pdv_diario_mensal(data_inicial, data_final, formato)
    if not ids_pedidos:
        return []

    resultados = []
    for pid in ids_pedidos:
        detalhes = obter_detalhes_pdv_mensal(pid, formato)
        if detalhes:
            resultados.append(detalhes)
        time.sleep(delay)  # pausa entre requisições

    return resultados
