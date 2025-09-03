import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from obter_clientes_vendedor import obter_relatorio_cliente_vendedor
from obter_clientes_vendedor import obter_dados_cliente_pedido

load_dotenv()

def relatorio_cliente_vendedor():
    
    id_vendedor = os.getenv("ID_VENDEDOR_K")
    
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
        
        print(f"- {cliente}: Última compra em {ultima_data_str} "
              f"({dias_sem_compra} dias atrás) -> {status} - Tel: {telefone} - CPF/CNPJ: {cpf_cnpj}") 

        dados_para_df.append({
            "Nome": cliente,
            "Última compra": ultima_data_str,
            "Dias sem compra": dias_sem_compra,
            "Situação": status,
            "Telefone": telefone,
            "Cpf/Cnpj": cpf_cnpj
        })
        
    print("🤖 Transformando esses dados em um arquivo no excell ...")
    df = pd.DataFrame(dados_para_df)
    
    df.to_excel("relatorio_clientes_vendedor_katlen.xlsx", index=False)
    print("Arquivo Excel criado: relatorio_clientes_vendedor.xlsx")
   
    
    
relatorio_cliente_vendedor()