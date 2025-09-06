import os
import glob
import pandas as pd
from datetime import datetime, timedelta
from src.robos.gerar_relatorio_clientes_dia import gerar_relatorios_cliente_dia

#E
def extraindo_ultimo_arquivo_dowloads():
    gerar_relatorios_cliente_dia()
    lista_arquivos = glob.glob("C:/Users/equip/Downloads/*")
    ultimo_arquivo_dowload = max(lista_arquivos, key=os.path.getmtime)
    print(ultimo_arquivo_dowload)
    df = pd.read_excel(ultimo_arquivo_dowload)
    return df
    
#T and L
def processando_planilha():
    df = extraindo_ultimo_arquivo_dowloads()
    
    colunas_excluir = [
        "Empresa lead 's", 
        "Empresa do contato", 
        "Criado por",
        "Modificado por",
        "Próxima tarefa",
        "Fechada em",
        "Profissão",
        "Técnicas",
        "Motivo Perda",
        "BOT|AutoLead",
        "BOT|Opção Bot",
        "BOT|Grupo Disparo",
        "BOT|Opção 1",
        "BOT|Opção 2",
        "BOT|Opção 3",
        "BOT|Opção 4",
        "BOT|Opção 5",
        "utm_content",
        "utm_medium",
        "utm_campaign",
        "utm_source",
        "utm_term",
        "utm_referrer",
        "referrer",
        "gclientid",
        "gclid",
        "fbclid",
        "Posição (contato)",
        "Email comercial (contato)",
        "Email pessoal (contato)",
        "Outro email (contato)",
        "Tel. direto com. (contato)",
        "Celular (contato)",
        "Faz (contato)",
        "Telefone residencial (contato)",
        "Outro telefone (contato)",
        "CPF/CNPJ (contato)",
        "Endereço (contato)",
        "Data de nascimento (contato)",
        "Termos do usuário (contato)",
        "Nota 1",
        "Nota 2",
        "Nota 3",
        "Nota 4",
        "Nota 5"
    ]
    
    df = df.drop(columns=colunas_excluir, errors="ignore")
    
    df['Ult.Interação'] = pd.to_datetime(df['Ult.Interação'], dayfirst=True)
    
    df['Ultima intereção'] = df['Ult.Interação'].dt.strftime("%d/%m/%Y")
    
    print(df)

    pasta_saida = ("C:/Users/equip/Documents/dev/planilhas/contatos_trabalhados_diario")
    os.makedirs(pasta_saida, exist_ok=True)
    
    data_anterior = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    caminho_arquivo = os.path.join(pasta_saida, f"Relatório_Clientes_Contactados_{data_anterior}.xlsx")
    
    df.to_excel(caminho_arquivo, index=False)
    
    print(f"Planilha salva em: {caminho_arquivo}")
    
processando_planilha()