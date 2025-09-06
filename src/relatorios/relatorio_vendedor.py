import os
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
from src.api.obter_clientes_vendedor import obter_dados_cliente_pedido
from src.api.obter_clientes_vendedor import obter_dados_contato_por_cpf
from src.api.obter_clientes_vendedor import obter_relatorio_cliente_vendedor

load_dotenv()

def relatorio_cliente_vendedor():
    
    id_vendedor = os.getenv("ID_VENDEDOR_V")
    
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
    
    df.to_excel("relatorio_clientes_vendedor_Vanessa.xlsx", index=False)
    print("Arquivo Excel criado: relatorio_clientes_vendedor.xlsx")
   
    
    
