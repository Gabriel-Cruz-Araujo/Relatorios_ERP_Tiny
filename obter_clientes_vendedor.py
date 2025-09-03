import os
import requests
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

TOKEN = os.getenv("TOKEN_API_TINY")
url_busca = "https://api.tiny.com.br/api2/pedidos.pesquisa.php"
url_busca_pedidos_id = "https://api.tiny.com.br/api2/pedido.obter.php"


def obter_relatorio_cliente_vendedor(vendedor_id, formato="JSON"):
    pagina = 1
    clientes_compras = defaultdict(list)

    while True:
        payload = {
            "token": TOKEN,
            "formato": formato,
            "idVendedor": vendedor_id,
            "pagina": pagina
        }

        response = requests.post(url_busca, data=payload)
        data = response.json()

        if "retorno" not in data or data["retorno"]["status"] != "OK":
            print(f"Erro na página {pagina}: {data}")
            break

        pedidos = data["retorno"].get("pedidos", [])
        if not pedidos:
            break

        for p in pedidos:
            pedido = p["pedido"]
            cliente_nome = pedido.get("nome")
            data_pedido = pedido.get("data_pedido")
            id_pedido = pedido.get("id")

            if cliente_nome and data_pedido and id_pedido:
                clientes_compras[cliente_nome].append({
                    "id_pedido": id_pedido,
                    "data_pedido": data_pedido
                })

        pagina += 1  # próxima página

    # pega a última compra de cada cliente
    clientes_ultima_compra = {}
    for cliente, compras in clientes_compras.items():
        ultima_compra = max(compras, key=lambda x: x["data_pedido"])
        clientes_ultima_compra[cliente] = ultima_compra

    return clientes_ultima_compra

def obter_dados_cliente_pedido(id_pedido, formato="JSON"):
    payload = {
        "token": TOKEN,
        "id": id_pedido,
        "formato": formato
    }

    response = requests.post(url_busca_pedidos_id, data=payload)
    data = response.json()

    if "retorno" not in data or data["retorno"]["status"] != "OK":
        print(f"Erro ao buscar pedido {id_pedido}: {data}")
        return None

    pedido = data["retorno"].get("pedido", {})
    cliente = pedido.get("cliente", {})


    nome_cliente = cliente.get("nome")
    telefone_cliente = cliente.get("fone")
    cpf_cliente = cliente.get("cpf_cnpj")

    return {
        "id_pedido": id_pedido,
        "cliente": nome_cliente,
        "telefone": telefone_cliente,
        "cpf_cnpj": cpf_cliente
    }

def obter_dados_contato_por_cpf(cpf: str) -> str:
    """
    Recebe CPF/CNPJ e retorna o tipo principal do contato no Tiny,
    ex: 'Cliente Home Care' ou 'Profissional'. Retorna 'Não definido' se não encontrado.

    """
    # 1) Buscar cliente pelo CPF
    url_busca = "https://api.tiny.com.br/api2/contatos.pesquisa.php"
    params_busca = {"cpf_cnpj": cpf, "token": TOKEN, "formato": "json"}
    response_busca = requests.get(url_busca, params=params_busca)

    if response_busca.status_code != 200:
        print(f"Erro ao buscar cliente: {response_busca.status_code} {response_busca.text}")
        return "Não definido"

    dados_busca = response_busca.json()
    contatos = dados_busca.get("retorno", {}).get("contatos", [])
    if not contatos:
        return "Não definido"

    cliente_id = contatos[0]["contato"]["id"]

    # 2) Buscar detalhes do cliente
    url_detalhe = "https://api.tiny.com.br/api2/contato.obter.php"
    params_detalhe = {"id": cliente_id, "token": TOKEN, "formato": "json"}
    response_detalhe = requests.get(url_detalhe, params=params_detalhe)

    if response_detalhe.status_code != 200:
        print(f"Erro ao detalhar cliente: {response_detalhe.status_code} {response_detalhe.text}")
        return "Não definido"

    dados_detalhe = response_detalhe.json()
    # print(dados_detalhe)
    contato = dados_detalhe.get("retorno", {}).get("contato", {})
    tipos_contato = contato.get("tipos_contato", [])
    celular_contato = contato.get("celular")
    
    
    # if tipos_contato:
    #     return celular_contato, tipos_contato
    if tipos_contato:
        tipos_lista = [d['tipo'].strip().title() for d in tipos_contato]
        tipos_str = ', '.join(tipos_lista)
        return {
            "celular_contato": celular_contato,
            "tipos_str": tipos_str
        }

    return {"celular_contato": None, "tipos_str": None}

    


if __name__ == "__main__":
    # id_vendedor = "711131091"
    # clientes = obter_relatorio_cliente_vendedor(id_vendedor)
    # print("Clientes, última compra e ID do pedido:")
    # for cliente, dados in clientes.items():
    #     print(f"- {cliente}: Última compra em {dados['data_pedido']} (Pedido ID: {dados['id_pedido']})")

    # id_pedido_teste = ""
    # dados = obter_dados_cliente_pedido(id_pedido_teste)
    # if dados:
    #     print(f"Pedido {dados['id_pedido']}: {dados['cliente']} - Tel: {dados['telefone']} - CPF/CNPJ {dados['cpf_cnpj']}")

    cpf_cliente = "027.652.374-17"
    dados_cliente = obter_dados_contato_por_cpf(cpf_cliente)
    print(dados_cliente)

