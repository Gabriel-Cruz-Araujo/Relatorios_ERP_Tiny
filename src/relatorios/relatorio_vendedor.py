import os
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
from src.utils.enviar_email import enviar_para_email_relatorio_vendedor
from src.api.obter_clientes_vendedor import obter_dados_cliente_pedido
from src.api.obter_clientes_vendedor import obter_dados_contato_por_cpf
from src.api.obter_clientes_vendedor import obter_relatorio_cliente_vendedor

load_dotenv()

pasta_destino = "C:/Users/equip/Documents/relatorios/relatorio_vendedores"
os.makedirs(pasta_destino, exist_ok=True)

data_hoje = datetime.now().strftime("%d-%m-%Y")

def relatorio_cliente_vendedor(escolha_vendedor):
    """
    Código para gerar a planilha dos clientes
    em relação ao vendedor selecionado.
    
    """
    if escolha_vendedor == 1:
        id_vendedor = os.getenv("ID_VENDEDOR_V")
    elif escolha_vendedor == 2:
        id_vendedor = os.getenv("ID_VENDEDOR_K")
    elif escolha_vendedor == 3:
        id_vendedor = os.getenv("ID_VENDEDOR_G")
        
    clientes = obter_relatorio_cliente_vendedor(id_vendedor)
    print("Clientes e data da última compra:")
    
    dados_para_df = []
    
    for cliente, dados in clientes.items():

        ultima_data_str = dados["data_pedido"]
        id_pedido = dados["id_pedido"]
        
        
        ultima_data = datetime.strptime(ultima_data_str, "%d/%m/%Y")
       
        dias_sem_compra = (datetime.today() - ultima_data).days
        
        status = "ATIVO" if dias_sem_compra <= 90 else "INATIVO" 
        
        telefone = None
        cpf_cnpj = None
        
        dados_cliente = obter_dados_cliente_pedido(id_pedido) 
        if dados_cliente:
            telefone = dados_cliente.get("telefone", "Não informado")
            cpf_cnpj = dados_cliente.get("cpf_cnpj", "Não informado")
        
        dados_complementares = obter_dados_contato_por_cpf(cpf_cnpj)
    
        if isinstance(dados_complementares, dict):  # garante que seja dict
            celular = dados_complementares.get("celular_contato", "Não informado")
            tipo = dados_complementares.get("tipos_str", "Não informado")
        else:
            celular = "Não informado"
            tipo = "Não informado"
            
        print(f"- {cliente}: Última compra em {ultima_data_str} "
              f"({dias_sem_compra} dias atrás) -> {status} - Tel: {telefone} - CPF/CNPJ: {cpf_cnpj} - Celular: {celular} - Tipos: {tipo}") 

        dados_para_df.append({
            "Cpf/Cnpj": cpf_cnpj,
            "Nome": cliente,
            "Última compra": ultima_data_str,
            "Dias sem compra": dias_sem_compra,
            "Telefone": telefone,
            "Celular": celular,
            "Situação": status,
            "Tags": tipo
            
        })
        
    print("🤖 Transformando esses dados em um arquivo no excell ...")
    df = pd.DataFrame(dados_para_df)
    
    if escolha_vendedor == 1:
        caminho_arquivo = os.path.join(pasta_destino, f"relatorio_clientes_Vanessa_{data_hoje}.xlsx")
        df.to_excel(caminho_arquivo, index=False)
        print("Arquivo Excel criado: relatorio_clientes_vendedor_Vanessa.xlsx")
        
    elif escolha_vendedor == 2:
        caminho_arquivo = os.path.join(pasta_destino, f"relatorio_clientes_Kattlen_{data_hoje}.xlsx")
        df.to_excel(caminho_arquivo, index=False)
        print("Arquivo Excel criado: relatorio_clientes_vendedor_Katllen.xlsx")
        
    elif escolha_vendedor == 3:
        caminho_arquivo = os.path.join(pasta_destino, f"relatorio_clientes_Gabriel_{data_hoje}.xlsx")
        df.to_excel(caminho_arquivo, index=False)
        print("Arquivo Excel criado: relatorio_clientes_vendedor_Gabriel.xlsx")
    
    
    
def relatorio_vendedores_autom():
    """
    Código para gerar o relatorio de todos os vendedores
    em excel unico para cada um e mandar por email.
    
    """
    
    vendedores = {
        # "Vanessa": os.getenv("ID_VENDEDOR_V"),
        "Kattlen": os.getenv("ID_VENDEDOR_K"),
        "Gabriel": os.getenv("ID_VENDEDOR_G"),
    }
    
    dados_para_df = []
    
    for nome_vendedor, id_vendedor in vendedores.items():
        clientes = obter_relatorio_cliente_vendedor(id_vendedor)
        print(f"\n=== Relatório de {nome_vendedor} ===")
        clientes = obter_relatorio_cliente_vendedor(id_vendedor)
        dados_para_df = []

        for cliente, dados in clientes.items():
            ultima_data_str = dados["data_pedido"]
            id_pedido = dados["id_pedido"]

            ultima_data = datetime.strptime(ultima_data_str, "%d/%m/%Y")
            dias_sem_compra = (datetime.today() - ultima_data).days

            status = "ATIVO" if dias_sem_compra <= 90 else "INATIVO"

            telefone = None
            cpf_cnpj = None

            dados_cliente = obter_dados_cliente_pedido(id_pedido)
            if dados_cliente:
                telefone = dados_cliente.get("telefone", "Não informado")
                cpf_cnpj = dados_cliente.get("cpf_cnpj", "Não informado")

            dados_complementares = obter_dados_contato_por_cpf(cpf_cnpj)
            if isinstance(dados_complementares, dict):
                celular = dados_complementares.get("celular_contato", "Não informado")
                tipo = dados_complementares.get("tipos_str", "Não informado")
            else:
                celular = "Não informado"
                tipo = "Não informado"

            dados_para_df.append({
                "Cpf/Cnpj": cpf_cnpj,
                "Nome": cliente,
                "Última compra": ultima_data_str,
                "Dias sem compra": dias_sem_compra,
                "Telefone": telefone,
                "Celular": celular,
                "Situação": status,
                "Tags": tipo
            })

        # cria o Excel separado para cada vendedor
        df = pd.DataFrame(dados_para_df)
        caminho_arquivo = os.path.join(pasta_destino, f"relatorio_clientes_{nome_vendedor}_{data_hoje}.xlsx")
        df.to_excel(caminho_arquivo, index=False)

        print(f"✅ Arquivo criado: {caminho_arquivo}")
        time.sleep(15)
    enviar_para_email_relatorio_vendedor()
if __name__ == "__main__":
    # relatorio_cliente_vendedor()  
    relatorio_vendedores_autom()  
   
    
    
