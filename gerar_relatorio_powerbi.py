from src.relatorios.relatorio_pedidos_de_venda_diario import relatorio_pdv_diario
from datetime import datetime
"""
Rotina que alimenta o 
painel do power bi

"""
data = datetime.now().strftime("%d-%m-%Y")

relatorio_pdv_diario(data)