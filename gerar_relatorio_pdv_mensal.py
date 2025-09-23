from src.relatorios.relatorio_pdvs_mensal import relatorio_pdv_mensal
from src.utils.obter_mes_atual import obter_datas_mes_atual


data_inicial, data_final = obter_datas_mes_atual()


relatorio_pdv_mensal(data_inicial, data_final)