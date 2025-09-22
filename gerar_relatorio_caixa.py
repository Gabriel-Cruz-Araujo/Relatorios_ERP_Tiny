from src.relatorios.relatorio_pedidos_de_venda_diario import relatorio_pdv_diario
from datetime import datetime, timedelta
from datetime import datetime
"""
Rotina que alimenta o 
painel do power bi e os caixas diarios

"""

ontem = datetime.now() - timedelta(days=1)
data_ontem = ontem.strftime("%d-%m-%Y")


relatorio_pdv_diario(data_ontem)